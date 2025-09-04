package mainPackage;

public class SubClass extends ParentClass {
    private String subVariable;

    public SubClass(int value, String variable, String subVariable) {
        super(value);
        this.subVariable = subVariable;
        System.out.println("子类变量的值为：" + this.subVariable);
    }
}