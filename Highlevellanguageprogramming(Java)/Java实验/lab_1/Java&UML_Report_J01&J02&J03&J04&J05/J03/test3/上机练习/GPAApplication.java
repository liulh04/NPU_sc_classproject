public class GPAApplication {
    public static void main(String[] args) {

        String studentName1 = "张一";
        double[] scores1 = {4.0, 71.5, 3.5, 80.4, 3.0, 95.5};


        double gpa1 = calculateGPA(studentName1, scores1);
        System.out.println(studentName1 + " 的GPA为：" + gpa1);


        String studentName2 = "李二";
        double[] scores2 = {4.0, 78.5, 3.0, 54.5, 3.0, 60.5};


        double gpa2 = calculateGPA(studentName2, scores2);
        System.out.println(studentName2 + " 的GPA为：" + gpa2);


        String studentName3 = "赵三";
        double[] scores3 = {4.0, 88.5, 3.5, 92.5, 3.0, 71.5};


        double gpa3 = calculateGPA(studentName3, scores3);
        System.out.println(studentName3 + " 的GPA为：" + gpa3);
    }

    public static double calculateGPA(String studentName, double[] scores) {
        double totalCredits = 0;
        double totalWeightedScore = 0;

        for (int i = 0; i < scores.length; i += 2) {
            double credit = scores[i];
            double score = scores[i + 1];
            double convertedScore = convertScore(score);

            totalCredits += credit;
            totalWeightedScore += convertedScore * credit;
        }

        double gpa = totalWeightedScore / totalCredits;
        return gpa;
    }

    public static double convertScore(double score) {
        if (score >= 85 && score <= 100) {
            return 4.0;
        } else if (score >= 75 && score <= 84) {
            return 3.0;
        } else if (score >= 60 && score <= 74) {
            return 2.0;
        } else if (score >= 45 && score <= 59) {
            return 1.0;
        } else {
            return 0.0;
        }
    }
}