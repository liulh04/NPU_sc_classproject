import java.util.Scanner;

public class StringToNumber {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("请输入一个字符串：");
        String input = scanner.nextLine();

        try {
            int number = Integer.parseInt(input);
            System.out.println("转换后的数字为：" + number);
        } catch (NumberFormatException e) {
            System.out.println("无法转换（有非数字字符）");
        } finally {
            System.out.println("程序结束。");
        }
    }
}