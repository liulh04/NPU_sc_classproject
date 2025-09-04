# Java第二次作业
--- 
 
---  

### 1.编写一个Java程序来打印一张脸  
解：  

    public class Main {
        public static void main(String[] args) {
        System.out.println("+“ ” “ ” +");
        System.out.println("[|0   0|]");
        System.out.println(" |  ^  |");
        System.out.println(" | '-' |");
        System.out.println("+--------+");
        }
    }  

### 2.显示以下main()例程将产生的确切输出
    public class Main {
        public static void main(String[] args) {
        int N;
        N=1;
        while(N<=32){
            N = 2 * N;
            System.out.println(N);
        }
        }
    }  
解：
输出：    

    2  
    4
    8
    16
    32
    64  

---  

### 3.显示以下main()例程将产生的确切输出

    public class Main {
        public static void main(String[] args) {
        int x,y;
        x=5;
        y=1;
        while(x>0){
        x=x-1;
        y=y*x;
        System.out.println(y);
        }
        }
    }
解：  

输出；  

    4 
    12
    24
    24
    0


### 4.写出下列程序结果：
  
    import java.io.*;
    public class Main {
        public static void main(String[] args) {
        int i,s=0;
        int a[]={10,20,30,40,50,60,70,80,90};
        for(i=0;i<a.length;i++)
            if(a[i]%3==0) s+=a[i];
        System.out.println("s="+s);
        }
    }

解： 

    s=180
  

### 5.有以下Java代码

  

    public class Main {
        public static void main(String[] args) {
        int a=0,b=5;
        String c[]={'A','b','C'};
        try{
            for(int i=1;i<4;i++){
                System.out.println(c[i]);
            }
            System.out.println(a/b+b/a);
        }
        catch (ArithmeticException e){
            System.out.println("D");
        }
        catch (ArrayIndexOutOfBoundsException e){
            System.out.println("E");
        }
        }
    }
解：  
    B
    C
    E    

  

### 6.有Java程序：

    public class Main {
        public static void main(String[] args) {
        int a=0,b=5;
        String c[]={"A","B","C"};
        try{
            System.out.println(c[a/b]);
            try{for(int i=1;i<4;i++){
                System.out.println(c[i]);
            }
            }
            catch (Exception e){
                System.out.println("D");
            }
            finally {
                System.out.println("E");
            }
            }
        catch (Exception e){
            System.out.println("F");
        }
    finally {
            System.out.println("G");
        }
        }
    }  

解：
A
B
C
D
E
G  

### 7.有以下Java代码：

    public class Main {
        static void my() throws ArithmeticException{
            System.out.println("A");
            throw new ArithmeticException("A");
        }

        public static void main(String[] args) {
            try{
                my();
            }
            catch (Exception e){
                System.out.println("B");

            }
            finally {
                System.out.println("C");
            }
        }
    }
解：
输出：A B C

---


© 2025 liulanker | [联系作者]( liulanker@gmail.com)