import java.util.concurrent.BlockingDeque;
import java.util.concurrent.LinkedBlockingDeque;

public class SharingSolver extends Solver implements Runnable {
    private static final BlockingDeque<Path> globalPathsQueue = new LinkedBlockingDeque<>();
    private static volatile int globalBestPathCost = Integer.MAX_VALUE;

    public SharingSolver(int vertices, int[][] costs) {
        super(vertices, costs);
    }

    @Override
    protected void broadcastBestPathCost() {
        globalBestPathCost = this.bestPathCost;
    }

    @Override
    protected void addPath(Path newPath) {
        globalPathsQueue.push(newPath);
    }

    @Override
    public void run() {
        try {
            while (true) {
                // daemon will work until main thread dies
                Path pathToTry = globalPathsQueue.takeFirst();
                // update local optimum based on global one from "scheduler"
                bestPathCost = globalBestPathCost;

                tryPath(pathToTry);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}
