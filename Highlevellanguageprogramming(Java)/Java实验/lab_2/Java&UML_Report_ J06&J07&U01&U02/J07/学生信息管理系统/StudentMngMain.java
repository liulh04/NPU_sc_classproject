import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Student implements Serializable {
    private static final long serialVersionUID = 1L;

    private String studentId;
    private String name;
    private String birthDate;
    private String gender;
    private String className;
    private String major;

    public Student(String studentId, String name, String birthDate, String gender, String className, String major) {
        this.studentId = studentId;
        this.name = name;
        this.birthDate = birthDate;
        this.gender = gender;
        this.className = className;
        this.major = major;
    }

    public String getStudentId() {
        return studentId;
    }

    public String getName() {
        return name;
    }

    public String getBirthDate() {
        return birthDate;
    }

    public String getGender() {
        return gender;
    }

    public String getClassName() {
        return className;
    }

    public String getMajor() {
        return major;
    }

    @Override
    public String toString() {
        return "Student{" +
                "studentId='" + studentId + '\'' +
                ", name='" + name + '\'' +
                ", birthDate='" + birthDate + '\'' +
                ", gender='" + gender + '\'' +
                ", className='" + className + '\'' +
                ", major='" + major + '\'' +
                '}';
    }
}

class StudentManager {
    private List<Student> studentList;

    public StudentManager() {
        studentList = new ArrayList<>();
    }

    public void addStudent(Student student) {
        studentList.add(student);
        System.out.println("学生信息添加成功！");
    }

    public Student findStudent(String studentId) {
        for (Student student : studentList) {
            if (student.getStudentId().equals(studentId)) {
                return student;
            }
        }
        return null;
    }

    public void deleteStudent(String studentId) {
        for (Student student : studentList) {
            if (student.getStudentId().equals(studentId)) {
                studentList.remove(student);
                System.out.println("学生信息删除成功！");
                return;
            }
        }
        System.out.println("找不到学号为 " + studentId + " 的学生信息！");
    }

    public void listAllStudents() {
        if (studentList.isEmpty()) {
            System.out.println("学生信息为空！");
        } else {
            for (Student student : studentList) {
                System.out.println(student);
            }
        }
    }

    public void saveToFile(String filename) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(studentList);
            System.out.println("学生信息保存成功！");
        } catch (IOException e) {
            System.out.println("保存学生信息失败：" + e.getMessage());
        }
    }

    public void loadFromFile(String filename) {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            studentList = (List<Student>) ois.readObject();
            System.out.println("学生信息加载成功！");
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("加载学生信息失败：" + e.getMessage());
        }
    }
}

public class StudentMngMain {
    public static void main(String[] args) {
        StudentManager studentManager = new StudentManager();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("学生信息管理系统");
            System.out.println("1. 添加学生信息");
            System.out.println("2. 查询学生信息");
            System.out.println("3. 删除学生信息");
            System.out.println("4. 列出所有学生信息");
            System.out.println("5. 保存学生信息到文件");
            System.out.println("6. 从文件加载学生信息");
            System.out.println("0. 退出系统");
            System.out.print("请输入指令：");

            int choice = scanner.nextInt();
            scanner.nextLine(); // 读取换行符

            switch (choice) {
                case 1:
                    System.out.print("请输入学号：");
                    String studentId = scanner.nextLine();
                    System.out.print("请输入姓名：");
                    String name = scanner.nextLine();
                    System.out.print("请输入出生日期：");
                    String birthDate = scanner.nextLine();
                    System.out.print("请输入性别：");
                    String gender = scanner.nextLine();
                    System.out.print("请输入班级：");
                    String className = scanner.nextLine();
                    System.out.print("请输入专业：");
                    String major = scanner.nextLine();

                    Student student = new Student(studentId, name, birthDate, gender, className, major);
                    studentManager.addStudent(student);

                    break;
                case 2:
                    System.out.print("请输入要查询的学号：");
                    String queryStudentId = scanner.nextLine();
                    Student queryStudent = studentManager.findStudent(queryStudentId);
                    if (queryStudent != null) {
                        System.out.println("查询结果：");
                        System.out.println(queryStudent);
                    } else {
                        System.out.println("找不到学号为 " + queryStudentId + " 的学生信息！");
                    }
                    break;
                case 3:
                    System.out.print("请输入要删除的学号：");
                    String deleteStudentId = scanner.nextLine();
                    studentManager.deleteStudent(deleteStudentId);
                    break;
                case 4:
                    studentManager.listAllStudents();
                    break;
                case 5:
                    System.out.print("请输入要保存到的文件名：");
                    String saveFilename = scanner.nextLine();
                    studentManager.saveToFile(saveFilename);
                    break;
                case 6:
                    System.out.print("请输入要加载的文件名：");
                    String loadFilename = scanner.nextLine();
                    studentManager.loadFromFile(loadFilename);
                    break;
                case 0:
                    System.out.println("感谢使用学生信息管理系统，拜拜~");
                    System.exit(0);
                default:
                    System.out.println("请重新输入！");
            }
        }
    }
}