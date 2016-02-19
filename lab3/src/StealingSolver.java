import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedDeque;

public class StealingSolver extends Solver implements Runnable {
    public volatile boolean isLookingForWork = false;
    private List<StealingSolver> otherSolvers;
    protected final Deque<Path> paths = new ConcurrentLinkedDeque<>();

    public StealingSolver(int vertices, int[][] costs) {
        super(vertices, costs);
    }

    @Override
    protected void broadcastBestPathCost() {
        otherSolvers.forEach(solver -> solver.updatePath(this.bestPathCost));
    }

    @Override
    protected void addPath(Path newPath) {
        this.paths.push(newPath);
    }

    public void setWorkers(List<StealingSolver> allWorkers) {
        otherSolvers = new ArrayList<>(allWorkers);
        otherSolvers.remove(this);
    }

    @Override
    public void run() {
        while (true) {
            Path pathToTry = paths.pollFirst();
            if (pathToTry == null) { // have to steal work
                isLookingForWork = true;

                pathToTry = getStolenPath();
                if (pathToTry == null) {
                    continue; // will need to try stealing again
                }
            }
            isLookingForWork = false;
            tryPath(pathToTry);
        }
    }

    private Path getStolenPath() {
        for (StealingSolver solver : otherSolvers) {
            Path stolenPath = solver.paths.pollFirst();
            if (stolenPath != null) {
                return stolenPath;
            }
        }
        return null;
    }
}
