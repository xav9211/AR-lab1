import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {

    private static void printExecutionFormat() {
        System.out.println("[problemFile] [numberOfThreads] [type]");
        System.out.println("type should be 'sharing' or 'stealing'");
        System.exit(1);
    }

    public static void main(String[] args) throws IOException {

        if (args.length < 3) {
            printExecutionFormat();
        }

        String fileName = args[0];
        int numberOfThreads = Integer.parseInt(args[1]);
        String typeOfWorker = args[2];
        if (!(typeOfWorker.equals("stealing") || typeOfWorker.equals("sharing"))) {
            printExecutionFormat();
        }

        BufferedReader matrixOfCostsReader = new BufferedReader(new FileReader(fileName));
        int numberOfVertices = Integer.parseInt(matrixOfCostsReader.readLine());
        long startTime = System.currentTimeMillis();
        int[][] costs = createCostsMatrix(matrixOfCostsReader, numberOfVertices);

        int initialBestPath;
        initialBestPath = calculateRandomCost(costs, numberOfVertices);
//        initialBestPath = calculateGreedyCost(costs, numberOfVertices);

        List<Path> initialPaths = new ArrayList<>();
        Path initialPath = new Path(0, numberOfVertices);
        for (int initialNode = 1; initialNode < numberOfVertices; initialNode++) {
            int addedCost = costs[0][initialNode];
            initialPaths.add(new Path(initialPath, initialNode, addedCost));
        }

        if (typeOfWorker.equals("stealing")) {
            System.out.println("Stealing");
            runStealingSolvers(numberOfThreads, numberOfVertices, startTime, costs, initialPaths, initialBestPath);
        }
        else
            runSharingSolvers(numberOfThreads, numberOfVertices, startTime, costs, initialPaths, initialBestPath);
    }

    private static int[][] createCostsMatrix(BufferedReader graph, int vertices) throws IOException {
        int[][] costs = new int[vertices][vertices];
        for (int i = 0; i < vertices; i++) {
            String costOfNeighbours = graph.readLine();
            List<Integer> readCostsOfNeighbours = Arrays.stream(costOfNeighbours.split("\\s+")).map(Integer::valueOf).collect(Collectors.toList());
            for (int j = 0; j < vertices; j++)
                costs[i][j] = readCostsOfNeighbours.get(j);
        }
        return costs;
    }

    private static int calculateRandomCost(int[][] costs, int vertices) {
        List<Integer> visited = new ArrayList<>();
        for (int i = 0; i < vertices; i++)
            visited.add(i);

        Collections.shuffle(visited);
        visited.add(visited.get(0));

        int sum = 0;
        for (int i = 0; i < visited.size() - 1; i++)
            sum += costs[visited.get(i)][visited.get(i+1)];

        return sum;
    }

    private static int calculateGreedyCost(int[][] costs, int vertices) {
        int minCost = Integer.MAX_VALUE;
        int[] visited = new int[vertices];
        int initialNode = 0;
        int lastNode = 0;

        //select first edge
        for (int i = 0; i < vertices; i++)
            for (int j = 0; j < vertices; j++)
                if (i != j && minCost > costs[i][j]) {
                    minCost = costs[i][j];
                    initialNode = i;
                    lastNode = j;
                }

        visited[initialNode] = visited[lastNode] = 1;

        //rest of edges
        int nextNode = 0;
        int cost = minCost;
        for (int i =0; i < vertices; i++) {
            minCost = Integer.MAX_VALUE;
            for (int j = 0; j < vertices; j++)
                if (visited[j] == 0 && minCost > costs[lastNode][j]) {
                    minCost = costs[lastNode][j];
                    nextNode = j;
                }
            visited[nextNode] = 1;
            lastNode = nextNode;
            cost += minCost;
        }

        //add to return to initial node
        cost += costs[lastNode][initialNode];
        return cost;
    }

    private static void runStealingSolvers(int numberOfThreads, int vertices, long startTime, int[][] costs, List<Path> initialPaths, int bestPath) {
        List<StealingSolver> solvers = Stream.generate(() -> new StealingSolver(vertices, costs)).limit(numberOfThreads).collect((Collectors.toList()));

        for (int i = 0; i < initialPaths.size(); i++)
            solvers.get(i % numberOfThreads).addPath(initialPaths.get(i));

        solvers.forEach(solver -> solver.setWorkers(solvers));
        solvers.forEach(solver -> solver.updatePath(bestPath));

        List<Thread> threads = solvers.stream().map(Thread::new).collect(Collectors.toList());
        threads.forEach(thread -> thread.setDaemon(true));
        threads.forEach(Thread::start);

        for (int blockedCount = 0; blockedCount < 5; ) { //approximation to see if max finished
            try {
                Thread.sleep(200);

                //if all are blocked
                if (solvers.stream().allMatch(solver -> solver.isLookingForWork))
                    blockedCount++;
                else
                    blockedCount = 0;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        printResults(solvers, numberOfThreads, System.currentTimeMillis() - startTime);
    }

    private static void runSharingSolvers(int numberOfThreads, int vertices, long startTime, int[][] costs, List<Path> initialPaths, int bestPath) {
        List<SharingSolver> solvers = Stream.generate(() -> new SharingSolver(vertices, costs)).limit(numberOfThreads).collect(Collectors.toList());

        solvers.forEach(solver -> solver.updatePath(bestPath));

        for (int i = 0; i < initialPaths.size(); i++) {
            solvers.get(i % numberOfThreads).addPath(initialPaths.get(i));
        }

        List<Thread> threads = solvers.stream().map(Thread::new).collect(Collectors.toList());
        threads.forEach(thread -> thread.setDaemon(true));
        threads.forEach(Thread::start);

        for (int blockedCount = 0; blockedCount < 5; ) { // approximation to see if all finished
            try {
                Thread.sleep(200);

                //if all Blocked
                if (threads.stream().allMatch(thread -> thread.getState() == Thread.State.BLOCKED ||
                        thread.getState() == Thread.State.WAITING)) {
//                    threads.forEach(thread -> System.out.print(thread.getState() + " "));
                    blockedCount++;
                } else {
                    blockedCount = 0;
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        printResults(solvers, numberOfThreads, System.currentTimeMillis() - startTime);
    }

    private static void printResults(List<? extends Solver> solvers, int numberOfThreads, long elapsedTime) {
        Optional<Path> globalBestPath = solvers.stream().filter(solver -> solver.bestPath != null)
                .map(solver -> {
//                    System.out.println(solver.bestPath.totalCost);
                    return solver.bestPath;
                }).min((s1, s2) -> s1.totalCost - s2.totalCost);

        globalBestPath.ifPresent(path -> {
//            System.out.println(path.totalCost + " " + path.vertexOrderToString());
            System.out.print(numberOfThreads + " " + path.totalCost + " " + elapsedTime + " ");
        });
        System.out.print(solvers.stream().map(solver -> String.valueOf(solver.getSolvedPaths())).collect(Collectors.joining(" ")) + " ");
        System.out.println(solvers.stream().map(solver -> String.valueOf(solver.getPrunedPaths())).collect(Collectors.joining(" ")));
    }

    public static void printCost(String nodes, int[][] costs) {
        List<Integer> nodeOrder = Arrays.stream(nodes.split("\\s+")).map(Integer::valueOf).collect(Collectors.toList());
        int sum = 0;
        for (int i = 0; i < nodeOrder.size() - 1; i++) {
            sum += costs[nodeOrder.get(i)][nodeOrder.get(i + 1)];
        }
        sum += costs[nodeOrder.size() - 1][nodeOrder.get(0)];
        System.out.println("TOTAL COST: " + sum);
    }
}
