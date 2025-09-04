package cn.crowdos.kernel.common;

import cn.crowdos.kernel.constraint.Condition;
import cn.crowdos.kernel.resource.AbstractParticipant;
import cn.crowdos.kernel.resource.ParticipantStatus;

public class PoiParticipant extends AbstractParticipant {
    @ability
    final PoiCondition activePoi; // POI条件

    // 构造函数，初始化参与者的位置
    public PoiParticipant(double latitude, double longitude) {
        this.activePoi = new PoiCondition(latitude, longitude); // 初始化 POI 条件
        status = ParticipantStatus.AVAILABLE; // 设置参与者状态为可用
    }

    // 判断是否有能力满足任务的 POI 条件
    @Override
    public boolean hasAbility(Class<? extends Condition> conditionClass) {
        return conditionClass == PoiCondition.class; // 判断是否支持 POI 条件
    }

    // 获取能力，如果是 POI 条件
    @Override
    public Condition getAbility(Class<? extends Condition> conditionClass) {
        if (!hasAbility(conditionClass)) // 如果不支持该能力，返回 null
            return null;
        else return activePoi; // 返回 POI 条件
    }

    @Override
    public String toString() {
        return "PoiParticipant{" + "latitude=" + activePoi.getLatitude() + ", longitude=" + activePoi.getLongitude() + "}"; // 返回 POI 信息
    }
}
