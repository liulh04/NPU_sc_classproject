package cn.crowdos.kernel.algorithms;

import cn.crowdos.kernel.constraint.Constraint;
import cn.crowdos.kernel.constraint.Coordinate;
import cn.crowdos.kernel.resource.Participant;
import cn.crowdos.kernel.resource.Task;
import cn.crowdos.kernel.system.SystemResourceCollection;
import cn.crowdos.kernel.system.resource.ParticipantPool;
import cn.crowdos.kernel.constraint.POIConstraint;

import java.util.*;
import java.util.stream.Collectors;

public class T_WeightFactory extends AlgoFactoryAdapter {

    public T_WeightFactory(SystemResourceCollection resourceCollection) {
        super(resourceCollection);
    }

    @Override
    public TaskAssignmentAlgo getTaskAssignmentAlgo() {
        return new TaskAssignmentAlgo() {
            @Override
            public List<List<Participant>> getAssignmentScheme(ArrayList<Task> tasks) {
                ParticipantPool participants = resourceCollection.getResourceHandler(ParticipantPool.class).getResourceView();

                // Location information for all tasks
                List<Coordinate> taskLocations = new ArrayList<>();
                // Location information of all candidates
                List<Coordinate> candidateLocations = new ArrayList<>();
                // Reserve all candidates
                List<Participant> candidates = new ArrayList<>();

                // Iterate over all tasks
                // The task constraints required in the algorithm are obtained, where is the task location
                for (Task task : tasks) {
                    List<Constraint> taskConstraint = task.constraints().stream()
                            .filter(constraint -> constraint instanceof POIConstraint)
                            .collect(Collectors.toList());
                    if (taskConstraint.size() != 1) {
                        return null;
                    }
                    Coordinate taskLocation = (Coordinate) taskConstraint.get(0);
                    // Add taskLocation to taskLocations
                    taskLocations.add(taskLocation);
                }

                for (Participant participant : participants) {
                    for (Task task : tasks) {
                        if (!task.canAssignTo(participant)) {
                            continue;
                        }
                        candidates.add(participant);
                        break;
                    }
                }

                // Get the number of tasks and the number of workers.
                int taskNum = tasks.size();
                int workerNum = candidates.size();

                // Iterate through the candidates to add their location information to candidateLocations
                for (Participant candidate : candidates) {
                    Coordinate candidateLocation = (Coordinate) candidate.getAbility(Coordinate.class);
                    candidateLocations.add(candidateLocation);
                }

                // Compute task-worker distance matrix
                double[][] distanceMatrix = new double[workerNum][taskNum];

                // Calculate the task-worker distance matrix based on candidateLocations and taskLocations
                for (int i = 0; i < workerNum; i++) {
                    for (int j = 0; j < taskNum; j++) {
                        distanceMatrix[i][j] = candidateLocations.get(i).euclideanDistance(taskLocations.get(j));
                    }
                }

                double[] taskScores = new double[taskNum];
                int[] p = new int[]{1};
                //initiallize taskscores
                for(int i=0; i < taskNum; i++)
                {
                    taskScores[i] = 1;
                }
                // Create an instance of T_Weight with appropriate parameters
                T_Weight t_weight = new T_Weight(workerNum, taskNum, distanceMatrix, taskScores, p, 1);

                // Assign tasks using T_Weight algorithm with a weight value (you need to define the weight value)
                t_weight.assignTasks(0.5);

                // Retrieve the task assignment results
                Map<Integer, List<Integer>> assignmentMap = t_weight.getAssignMap();

                // Prepare the assignmentScheme list
                List<List<Participant>> assignmentScheme = new ArrayList<>(taskNum);

                // Convert the assignment results to the required format
                for (int taskId = 0; taskId < taskNum; taskId++) {
                    List<Integer> assignedWorkers = assignmentMap.get(taskId);
                    List<Participant> assignedParticipants = new ArrayList<>();
                    for (Integer workerIndex : assignedWorkers) {
                        assignedParticipants.add(candidates.get(workerIndex));
                    }
                    assignmentScheme.add(assignedParticipants);
                }

                return assignmentScheme;
            }

            @Override
            public List<Participant> getAssignmentScheme(Task task) {
                // Implement the single-task assignment here using T_Weight algorithm

                // Retrieve task's location
                Coordinate taskLocation = null;  // Set this to the task's location
                if (task.constraints().size() != 1) {
                    return null;
                }

                // Retrieve the participants who can perform the task
                ParticipantPool participants = resourceCollection.getResourceHandler(ParticipantPool.class).getResourceView();
                List<Participant> candidates = participants.stream()
                        .filter(task::canAssignTo)
                        .collect(Collectors.toList());
                int workerNum = candidates.size();

                // Prepare the distance matrix for the single task assignment
                double[][] distanceMatrix = new double[workerNum][1];

                // Calculate distances based on task and candidate locations
                double[] taskScores = new double[]{1};
                int[] p = new int[]{1};
                // Create an instance of T_Weight with appropriate parameters
                T_Weight t_weight = new T_Weight(workerNum, 1, distanceMatrix, taskScores, p, 1);

                // Assign the single task using T_Weight algorithm with a weight value (you need to define the weight value)
                t_weight.assignTasks(0.5);

                // Retrieve the task assignment results
                Map<Integer, List<Integer>> assignmentMap = t_weight.getAssignMap();

                // Prepare the assignmentScheme list
                List<Participant> assignmentScheme = new ArrayList<>();

                // Convert the assignment results to the required format
                List<Integer> assignedWorkers = assignmentMap.get(0);  // Since there is only one task
                for (Integer workerIndex : assignedWorkers) {
                    assignmentScheme.add(candidates.get(workerIndex));
                }

                return assignmentScheme;
            }
        };
    }
}
