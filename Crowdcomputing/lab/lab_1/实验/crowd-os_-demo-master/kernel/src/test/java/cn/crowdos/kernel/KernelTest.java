package cn.crowdos.kernel;

import cn.crowdos.kernel.common.TimeParticipant;
import cn.crowdos.kernel.constraint.InvalidConstraintException;
import cn.crowdos.kernel.constraint.SimpleTimeConstraint;
import cn.crowdos.kernel.resource.Participant;
import cn.crowdos.kernel.resource.SimpleTask;
import cn.crowdos.kernel.resource.Task;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;

public class KernelTest {
    CrowdKernel kernel;

    @BeforeEach
    void setUp() {
        kernel = Kernel.getKernel();
        kernel.initial();

        // 创建并注册原有的两个参与者
        TimeParticipant p1 = new TimeParticipant("2024.6.1");
        TimeParticipant p2 = new TimeParticipant("2024.6.2");
        kernel.registerParticipant(p1);
        kernel.registerParticipant(p2);

        // 创建并注册 5 个新的参与者
        TimeParticipant p3 = new TimeParticipant("2024.6.3");
        TimeParticipant p4 = new TimeParticipant("2024.6.4");
        TimeParticipant p5 = new TimeParticipant("2024.6.5");
        TimeParticipant p6 = new TimeParticipant("2024.6.6");
        TimeParticipant p7 = new TimeParticipant("2024.6.7");
        kernel.registerParticipant(p3);
        kernel.registerParticipant(p4);
        kernel.registerParticipant(p5);
        kernel.registerParticipant(p6);
        kernel.registerParticipant(p7);

        // 创建并提交一个任务
        try {
            SimpleTimeConstraint timeConst = new SimpleTimeConstraint("2024.6.1", "2024.6.2");
            SimpleTask t1 = new SimpleTask(Collections.singletonList(timeConst), Task.TaskDistributionType.RECOMMENDATION);
            timeConst = new SimpleTimeConstraint("2024.5.28", "2024.6.2");
            SimpleTask t2 = new SimpleTask(Collections.singletonList(timeConst), Task.TaskDistributionType.RECOMMENDATION );
            kernel.submitTask(t1);
            kernel.submitTask(t2);

            // 创建并提交新的任务
            SimpleTimeConstraint timeConstNew = new SimpleTimeConstraint("2024.6.3", "2024.6.7");
            SimpleTask t3 = new SimpleTask(Collections.singletonList(timeConstNew), Task.TaskDistributionType.RECOMMENDATION);
            kernel.submitTask(t3); // 提交新的任务
        } catch (InvalidConstraintException e) {
            throw new RuntimeException(e);
        }
    }

    @AfterEach
    void tearDown() {
        Kernel.shutdown();
    }

    @Test
    void getTasks() {
        System.out.println(kernel.getTasks());
    }

    @Test
    void getParticipants() {
        System.out.println(kernel.getParticipants());
    }

    @Test
    void getTaskRecommendationScheme() {
        for (Task task : kernel.getTasks()) {
            System.out.println(kernel.getTaskRecommendationScheme(task));
        }
    }
}
