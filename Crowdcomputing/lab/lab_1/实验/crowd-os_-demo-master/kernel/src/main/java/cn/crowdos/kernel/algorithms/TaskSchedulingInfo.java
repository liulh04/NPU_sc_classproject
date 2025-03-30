package cn.crowdos.kernel.algorithms;

public class TaskSchedulingInfo {
    private int timeSlice;  // 时间片
    private long waitingTime;  // 等待时间
    private int executedCount;  // 任务执行完成的次数
    private int interruptedCount;  // 任务被中断的次数

    public TaskSchedulingInfo(int initialTimeSlice) {
        this.timeSlice = initialTimeSlice;
        this.waitingTime = 0;
        this.executedCount = 0;
        this.interruptedCount = 0;
    }

    public void decrementTimeSlice() {
        if (this.timeSlice > 0) {
            this.timeSlice--;
        }
    }

    public boolean isTimeSliceExpired() {
        return this.timeSlice <= 0;
    }

    public void incrementWaitingTime(long increment) {
        this.waitingTime += increment;
    }

    public long getWaitingTime() {
        return this.waitingTime;
    }

    public void incrementExecutedCount() {
        this.executedCount++;
    }

    public void incrementInterruptedCount() {
        this.interruptedCount++;
    }

    public void resetTimeSlice(int newTimeSlice) {
        this.timeSlice = newTimeSlice;
    }

    // 根据任务的执行情况动态调整时间片
    public void adjustTimeSlice() {
        if (this.interruptedCount > this.executedCount) {
            this.timeSlice = Math.min(this.timeSlice + 5, 100);  // 增加时间片，不超过最大值100
        } else if (this.executedCount > this.interruptedCount) {
            this.timeSlice = Math.max(this.timeSlice - 5, 10);  // 减少时间片，不低于最小值10
        }
        // 重置计数器
        this.executedCount = 0;
        this.interruptedCount = 0;
    }
}



