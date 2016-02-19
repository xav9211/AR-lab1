import java.util.Arrays;

public class Path {
    // index is node id, value is order when was the node visited
    public final int[] visitTime;
    public final int initialNode;
    public final int lastProcessedNode;
    public final int processedNodes;
    public final int totalCost;

    public Path(int initialNode, int nodes) {
        visitTime = new int[nodes];
        visitTime[initialNode] = 1;
        lastProcessedNode = initialNode;
        this.initialNode = initialNode;
        processedNodes = 1;
        totalCost = 0;
    }

    public Path(Path fromSolution, int toNode, int addedCost) {
        visitTime = Arrays.copyOf(fromSolution.visitTime, fromSolution.visitTime.length);
        processedNodes = fromSolution.processedNodes + 1;
        lastProcessedNode = toNode;
        visitTime[toNode] = processedNodes;
        totalCost = fromSolution.totalCost + addedCost;
        initialNode = fromSolution.initialNode;
    }

    public String vertexOrderToString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < processedNodes; i++) {
            for (int node = 0; node < visitTime.length; node++) {
                if (visitTime[node] == i) {
                    sb.append(node).append(" ");
                    break;
                }
            }
        }
        return sb.toString();
    }

    public String toString() {
        return "Solution cost: " + totalCost + " [" + vertexOrderToString() + "]";
    }
}
