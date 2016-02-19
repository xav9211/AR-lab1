
public abstract class Solver {
    private final int vertices;
    private int[][] costs;

    protected int bestPathCost = Integer.MAX_VALUE;
    protected Path bestPath = null;
    private long solvedPaths = 0;
    private long prunedPaths = 0;

    public Solver(int vertices, int[][] costs) {
        this.vertices = vertices;
        this.costs = costs;
    }

    public void tryPath(Path path) {

        solvedPaths++;

        int previousNode = path.lastProcessedNode;
        if (path.processedNodes == vertices) {
            addConnectionToCreateCycle(path, costs[previousNode][path.initialNode]);
        }
        if (path.processedNodes == vertices + 1) {
            updateBestPathIfBetter(path);
            return;
        }
        // check if already more expensive
        if (path.totalCost > bestPathCost) {
            prunedPaths++;
            return;
        }

        addAllPathsToQueue(path, previousNode);
    }


    private void addConnectionToCreateCycle(Path path, int addedCost) {
        addPath(new Path(path, path.initialNode, addedCost));
    }

    private void updateBestPathIfBetter(Path path) {
        if (path.totalCost < bestPathCost) { // update best path cost
//            System.out.println(path.totalCost + " IS THE BEST PATH");
            this.bestPath = path;
            bestPathCost = path.totalCost;
            broadcastBestPathCost();
        }
    }

    private void addAllPathsToQueue(Path path, int previousNode) {
        for (int toNode = 0; toNode < vertices; toNode++) {
            if (path.visitTime[toNode] == 0) { // it wasn't visited yet
                int addedCost = costs[previousNode][toNode];
                Path newPath = new Path(path, toNode, addedCost);
                addPath(newPath);
            }
        }
    }

    public synchronized void updatePath(int bestPathCost) {
        if (bestPathCost < this.bestPathCost) {
            this.bestPathCost = bestPathCost;
        }
    }

    public long getSolvedPaths() {
        return solvedPaths;
    }

    public long getPrunedPaths() {
        return prunedPaths;
    }

    protected abstract void broadcastBestPathCost();

    protected abstract void addPath(Path newPath);
}
