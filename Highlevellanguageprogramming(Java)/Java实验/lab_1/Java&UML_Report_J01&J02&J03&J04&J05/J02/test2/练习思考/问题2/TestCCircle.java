class CCircle {
    final double pi = 3.14159;
    double radius;

    double getRadius() {
        return radius;
    }

    void setCircle(double r) {
        radius = r;
    }

    double getArea() {
        return pi * radius * radius;
    }
}

public class TestCCircle {
    public static void main(String args[]) {
        CCircle cir1 = new CCircle();
        cir1.setCircle(2.0);
        System.out.println("radius = " + cir1.getRadius());
        System.out.println("area = " + cir1.getArea());
    }
}