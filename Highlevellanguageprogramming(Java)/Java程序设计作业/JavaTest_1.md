# Java第一次作业
---
 


### 1.给出以下的计算结果：
- 8>>1
- 8>>>1
- -8>>>1
- int i = 5/0.1

解：  
8>>1 = 4  
8>>>1 =4  
-8>>>1=124  注：(默认8位)  
java: ArithmeticException异常 ;不兼容的类型: 从double转换到int可能会有损失


--- 

### 2.请定义Student类。它包含：姓名，长度为8的字符串；学号，整型；班级，整型；是否党员，布尔型；平均成绩，单精度浮点数。
解：

    public class Student {
        private String name; // 姓名
        private int studentID; // 学号
        private int classID; // 班级
        private boolean isPartyMember; // 是否党员
        private float averageScore; // 平均成绩
    }
---
### 3.写出以下表达式的值
- （101+0）/3
- 3.0e-6*10000000.1
- true && true
- false && true
- (false&&false)||(true && true)
- (false||false)&&(true && true)
  
解：   
(101+0)/3 = 33  
3.0e-6*10000000.1 = 30.0000003    
true && true = true  
false && true = false  
(false&&false)||(true && true) = true  
(false||false)&&(true && true) = false


---


© 2025 liulanker | [联系作者]( liulanker@gmail.com)