package cn.crowdos.kernel.resource;

import cn.crowdos.kernel.Decomposable;
import cn.crowdos.kernel.constraint.Constraint;
import org.springframework.stereotype.Repository;

import java.util.List;
@Repository
public interface Task extends Decomposable<Task> {

    // Defining a new type called `TaskDistributionType` with two possible values: `ASSIGNMENT` and `RECOMMENDATION`.
    enum TaskDistributionType{
        ASSIGNMENT,
        RECOMMENDATION,
    }

    // Defining a new type called `TaskStatus` with three possible values: `READY`, `IN_PROGRESS`, and `FINISHED`.
    //Added a new type: 'INTERRUPTED'.
    enum TaskStatus {
        READY,
        IN_PROGRESS,
        INTERRUPTED,
        FINISHED,
    }

    /**
     * Returns the type of task distribution used in the simulation
     *
     * @return The task distribution type.
     */
    TaskDistributionType getTaskDistributionType();

    /**
     * Returns the status of the task.
     *
     * @return The task status is being returned.
     */
    TaskStatus getTaskStatus();



    /**
     * Sets the status of the task to the given status.
     *
     * @param status The status of the task.
     */
    void setTaskStatus(TaskStatus status);
    /**
     * Returns a list of constraints that are applied to the field.
     *
     * @return A list of constraints.
     */
    List<Constraint> constraints();

    /**
     * Returns true if the given participant can be assigned to this role.
     *
     * @param participant The participant to assign the task to.
     * @return A boolean value.
     */
    boolean canAssignTo(Participant participant);

    /**
     * Returns true if the type is assignable to the type of the given object.
     *
     * @return A boolean value.
     */
    boolean assignable();

    /**
     * Returns true if the game is over, false otherwise.
     *
     * @return A boolean value.
     */
    boolean finished();

}
