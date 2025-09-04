package cn.crowdos.kernel.algorithms;

import java.util.*;
import java.util.function.Supplier;
import java.util.stream.IntStream;

public class T_Weight {
    private int workerNum;
    private int taskNum;
    private double[][] distanceMatrix;
    private double[] taskScores;
    private int[] p;
    private int q;
    private Map<Integer, List<Integer>> assignMap = new HashMap<>();
    private double distance;
    private double score;

    public T_Weight(int workerNum, int taskNum, double[][] distanceMatrix, double[] taskScores, int[] p, int q) {
        this.workerNum = workerNum;
        this.taskNum = taskNum;
        this.distanceMatrix = distanceMatrix;
        this.taskScores = taskScores;
        this.p = p;
        this.q = q;
        for (int i = 0; i < workerNum; i++) {
            assignMap.put(i, new ArrayList<>());
        }
    }

    /**
     * Assign tasks to workers based on the weighted distance matrix.
     *
     * @param weight the weight parameter to determine the importance of distance and task scores in the assignment
     */
    public void assignTasks(double weight) {
        // Calculate the weighted distance matrix
        double[][] weightedDistanceMatrix = calculateWeightedDistanceMatrix(distanceMatrix, taskScores, weight);

        // Perform task assignment
        for (int i = 0; i < taskNum; i++) {
            int[] sortedWorkers = sortWorkersByDistance(weightedDistanceMatrix, i);
            for (int j = 0; j < p[i]; j++) {
                int workerIndex = sortedWorkers[j % sortedWorkers.length];
                assignMap.get(workerIndex).add(i);
            }
        }

        // Calculate the total distance and score
        calculateTotalDistance();
        calculateTotalScore();
    }

    /**
     * Calculate the weighted distance matrix by adding the task scores weighted by the given weight to the original distance matrix.
     *
     * @param distanceMatrix the original distance matrix between workers and tasks
     * @param taskScores     the scores of the tasks
     * @param weight         the weight parameter to determine the importance of distance and task scores
     * @return the weighted distance matrix
     */
    private double[][] calculateWeightedDistanceMatrix(double[][] distanceMatrix, double[] taskScores, double weight) {
        int n = distanceMatrix.length;
        int m = distanceMatrix[0].length;
        double[][] weightedDistanceMatrix = new double[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                weightedDistanceMatrix[i][j] = distanceMatrix[i][j] + weight * taskScores[j];
            }
        }
        return weightedDistanceMatrix;
    }

    /**
     * Sort the workers based on their distances to the given task in the weighted distance matrix.
     *
     * @param weightedDistanceMatrix the weighted distance matrix
     * @param taskIndex              the index of the task
     * @return an array of worker indices sorted by their distances to the task
     */
    private int[] sortWorkersByDistance(double[][] weightedDistanceMatrix, int taskIndex) {
        Integer[] workers = IntStream.range(0, workerNum)
                .boxed()
                .sorted(Comparator.comparingDouble(worker -> weightedDistanceMatrix[worker][taskIndex]))
                .toArray(Integer[]::new);

        return Arrays.stream(workers)
                .mapToInt(Integer::intValue)
                .toArray();
    }


    /**
     * Calculate the total distance by summing the distances traveled by workers to complete their assigned tasks.
     */
    private void calculateTotalDistance() {
        distance = 0;
        for (int workerIndex : assignMap.keySet()) {
            List<Integer> taskList = assignMap.get(workerIndex);
            for (int i = 0; i < taskList.size() - 1; i++) {
                int task1 = taskList.get(i);
                int task2 = taskList.get(i + 1);
                distance += distanceMatrix[workerIndex][task1] + distanceMatrix[workerIndex][task2];
            }
        }
    }

    /**
     * Calculate the total score by summing the scores of the assigned tasks.
     */
    private void calculateTotalScore() {
        score = 0;
        for (int workerIndex : assignMap.keySet()) {
            List<Integer> taskList = assignMap.get(workerIndex);
            for (int taskIndex : taskList) {
                score += taskScores[taskIndex];
            }
        }
    }

    /**
     * Print the assignment map, showing the tasks assigned to each worker.
     */
    public void printAssignMap() {
        for (int workerIndex : assignMap.keySet()) {
            List<Integer> taskList = assignMap.get(workerIndex);
            System.out.println("Worker " + workerIndex + " is assigned tasks: " + taskList);
        }
    }

    /**
     * Get the total distance traveled by workers to complete their assigned tasks.
     *
     * @return the total distance
     */
    public double getDistance() {
        return distance;
    }

    /**
     * Get the total score of the assigned tasks.
     *
     * @return the total score
     */
    public double getScore() {
        return score;
    }


    public Map<Integer, List<Integer>> getAssignMap() {
        return assignMap;
    }
}
