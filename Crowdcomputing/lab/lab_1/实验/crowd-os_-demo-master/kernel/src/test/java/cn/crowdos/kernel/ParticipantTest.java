package cn.crowdos.kernel;

import cn.crowdos.kernel.common.PoiParticipant;
import cn.crowdos.kernel.constraint.InvalidConstraintException;
import cn.crowdos.kernel.constraint.SimpleTimeConstraint;
import cn.crowdos.kernel.resource.SimpleTask;
import cn.crowdos.kernel.resource.Task;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Collections;

public class ParticipantTest {
    CrowdKernel kernel;

    @BeforeEach
    void setUp() {
        kernel = Kernel.getKernel();
        kernel.initial();

        // 创建并注册原有的两个参与者
        PoiParticipant p1 = new PoiParticipant(39.9, 116.4); // Beijing
        PoiParticipant p2 = new PoiParticipant(34.05, -118.25); // Los Angeles
        kernel.registerParticipant(p1);
        kernel.registerParticipant(p2);

        // 创建并提交任务
        try {
            SimpleTimeConstraint timeConst = new SimpleTimeConstraint("2024.6.1", "2024.6.2");
            SimpleTask t1 = new SimpleTask(Collections.singletonList(timeConst), Task.TaskDistributionType.RECOMMENDATION);
            kernel.submitTask(t1);
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
}
