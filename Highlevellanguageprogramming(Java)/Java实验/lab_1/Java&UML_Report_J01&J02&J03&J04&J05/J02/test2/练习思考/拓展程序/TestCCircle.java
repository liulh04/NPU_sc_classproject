class CCircle {
    final double pi = 3.14159; 
    
    double radius;
    
    CCircle(double r) {         radius = r;
    }
    
    double getRadius() {
        return radius;
    }
    
    double getArea() {         return pi * radius * radius;
    }
}

public class TestCCircle {
    public static void main(String args[]) {
        CCircle cir1 = new CCircle(2.0); 
        System.out.println("radius= " + cir1.getRadius());
        System.out.println("square = " + cir1.getArea());
    }
}