interface Vehicle {
    void start();

    void stop();
}

class Bike implements Vehicle {
    @Override
    public void start() {
        System.out.println("自行车启动");
    }

    @Override
    public void stop() {
        System.out.println("自行车停止");
    }
}

class Bus implements Vehicle {
    @Override
    public void start() {
        System.out.println("公交车启动");
    }

    @Override
    public void stop() {
        System.out.println("公交车停止");
    }
}

public class InterfaceDemo {
    public static void main(String[] args) {
        Bike myBike = new Bike();
        myBike.start();
        myBike.stop();

        Bus myBus = new Bus();
        myBus.start();
        myBus.stop();
    }
}