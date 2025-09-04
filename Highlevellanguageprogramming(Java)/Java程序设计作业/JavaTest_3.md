# Java第三次作业
--- 
## 姓名：刘力豪  学号；2022303210
---  

### 1.求出e = 1 + 1/1！ + 1/2！+ 1/3！+ ... 1/n! + ... 的近似值，要求误差小于0.0001，提示：：n越大误差越小，使用double型  


    public class Main {
        public static void main(String[] args) {
            int n = 0;
            double term = 1.0;
            double eApproximation = 1.0;

            while (term >= 0.0001) {
                n++;
                term /= n;
                eApproximation += term;
            }

            System.out.println("e 的近似值为: " + eApproximation);
        }
    }
  
---
### 2.代码执行后的输出结果是 10

    public class Main {
        public static void main(String[] args) {
        int percent = 10 ;
        tripleVale(percent);
        System.out.println(percent);
        }

        public static  void  tripleVale(int x){
            x=3*x;
            
        }
    }  
  
解： 结果是10  

---


### 3.给出如下Java代码

    public class Main {
        public static void main(String[] args) {
        int a=0,b=5;
        try{
            System.out.println(a/b+b/a);
            
        }
        catch {
            System.out.println("Exceptions!!!");
            }
        
        }
    }

解：因为catch后面缺少异常的类型说明，会出现的错误是 

    Main.java:10: error: reached end of file while parsing
         catch  

答案是E.None of the above  

---
### 4.有以下Java代码：
    class B extends  Exception{
    }
    class C extends B{

    }
    class D extends  C{
    }
    public class Main {
        public static void main(String[] args) {
            int a,b,c,d,x,y,z;
            a = b = c = d = x =  y =0;
            z=1;
            try {
                try {
                    switch (z){
                        case 1:throw new B();
                        case 2:throw new C();
                        case 3:throw new D();
                        case 4:throw new Exception();

                    }
                    a++;

                }
                catch (C e){
                    b++;
                }
                finally {
                    c++;
                }

            }
            catch (B e){
                d++;
            }
            catch (Exception e){
                x++;
            }
            finally {
                y++;
            }
            System.out.println(a+","+b+","+c+","+d+","+x+","+y);

        }
    }  


解：
编译并执行代码会出现结果是：0，0，1，1，0，1



---

### 5.有以下Java代码：

    public class Main {
        public static void main(String[] args) {
            int a =1,b=0;
            int c[]={1,2,3};
            try {
                System.out.println(c[1]);
                try {
                    System.out.println(a/b+b/a);
                }
                catch (ArithmeticException e){
                    System.out.println("C");
                }
                
            }
            catch (ArrayIndexOutOfBoundsException e){
                System.out.println("A");
            }
            finally {
                System.out.println("B");
            }
            
        }
    }  


解：编译并执行代码会出现：2BC


---


© 2025 liulanker | [联系作者]( liulanker@gmail.com)