# Java第四次作业
--- 

---  

### 1.写出下列程序的运行结果：

    import java.io.*;//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
    public class Main {
        public static void main(String[] args) {
            AB s = new AB("Hello!","I love JA V A.");
            System.out.println(s.toString());

        }
    }
    class AB {
        String s1;
        String s2;
        public AB(String str1,String str2){
        s1=str1;
        s2=str2;
        }
        public String toString(){
            return  s1+s2;
        }
    }


解：结果是：
Hello!I love JA V A.

---
### 2.给出下面代码的输出结果：

    public class Main {
        public static void main(String[] args) {
            new Main();
        }

        static int num = 4;

        {
            num += 3;
            System.out.println("b");
        }

        int a = 5;

        {
            System.out.println("c");
        }

        Main() {
            System.out.println("d");
        }

        static {
            System.out.println("a");
        }

        static void run() {
            System.out.println("e");
        }
    }

解： 结果是：
a
b
c
d
   

---  
### 3.给出下面代码的输出结果：
    public class Main  {
        private static  int a ;
        public static void main(String[] args ){
            modify(a);
            System.out.println(a);
        }
        public static void modify(int a){
            a++;
            
        }
    }

解：结果是：  
0  


  
--- 
  
### 4.声明测试一个复数类，其方法包括toString()以及复数的加减乘除运算

    class ComplexNumber {
        private double real;
        private double imaginary;

        public ComplexNumber(double real, double imaginary) {
            this.real = real;
            this.imaginary = imaginary;
        }

        public ComplexNumber add(ComplexNumber other) {
            double newReal = this.real + other.real;
            double newImaginary = this.imaginary + other.imaginary;
            return new ComplexNumber(newReal, newImaginary);
        }

        public ComplexNumber subtract(ComplexNumber other) {
            double newReal = this.real - other.real;
            double newImaginary = this.imaginary - other.imaginary;
            return new ComplexNumber(newReal, newImaginary);
        }

        public ComplexNumber multiply(ComplexNumber other) {
            double newReal = this.real * other.real - this.imaginary * other.imaginary;
            double newImaginary = this.real * other.imaginary + this.imaginary * other.real;
            return new ComplexNumber(newReal, newImaginary);
        }

        public ComplexNumber divide(ComplexNumber other) {
            double divisor = other.real * other.real + other.imaginary * other.imaginary;
            double newReal = (this.real * other.real + this.imaginary * other.imaginary) / divisor;
            double newImaginary = (this.imaginary * other.real - this.real * other.imaginary) / divisor;
            return new ComplexNumber(newReal, newImaginary);
        }

        @Override
        public String toString() {
            if (imaginary >= 0) {
                return real + " + " + imaginary + "i";
            } else {
                return real + " - " + (-imaginary) + "i";
            }
        }
    }

    public class Main {
        public static void main(String[] args) {
            ComplexNumber a = new ComplexNumber(3, 2);
            ComplexNumber b = new ComplexNumber(1, -4);

            ComplexNumber sum = a.add(b);
            ComplexNumber difference = a.subtract(b);
            ComplexNumber product = a.multiply(b);
            ComplexNumber quotient = a.divide(b);

            System.out.println("a: " + a);
            System.out.println("b: " + b);
            System.out.println("Sum: " + sum);
            System.out.println("Difference: " + difference);
            System.out.println("Product: " + product);
            System.out.println("Quotient: " + quotient);
        }
    }



---
    
    
© 2025 liulanker | [联系作者]( liulanker@gmail.com)