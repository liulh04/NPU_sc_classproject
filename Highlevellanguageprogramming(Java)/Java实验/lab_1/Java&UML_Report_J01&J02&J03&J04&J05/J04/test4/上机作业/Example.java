class People {
    protected double weight, height;

    public void speakHello() {
        System.out.println("yayawawa");
    }

    public void averageHeight() {
        height = 173;
        System.out.println("average height: " + height);
    }

    public void averageWeight() {
        weight = 70;
        System.out.println("average weight: " + weight);
    }
}

class ChinaPeople extends People {
    @Override
    public void speakHello() {
        System.out.println("你好，吃饭了吗");
    }

    @Override
    public void averageHeight() {
        System.out.println("中国人的平均身高：173.0厘米");
    }

    @Override
    public void averageWeight() {
        System.out.println("中国人的平均体重：67.34公斤");
    }

    public void chinaGongfu() {
        System.out.println("坐如钟，站如松，睡如弓");
    }
}

class AmericanPeople extends People {
    @Override
    public void speakHello() {
        System.out.println("How do you do");
    }

    @Override
    public void averageHeight() {
        
        super.averageHeight();
    }

    @Override
    public void averageWeight() {
         
        super.averageWeight();
    }

    public void americanBoxing() {
        System.out.println("直拳、勾拳");
    }
}

class BeijingPeople extends ChinaPeople {
    @Override
    public void speakHello() {
        System.out.println("您好，这里是北京");
    }

    @Override
    public void averageHeight() {
         
        super.averageHeight();
    }

    @Override
    public void averageWeight() {
        
        super.averageWeight();
    }

    public void beijingOpera() {
        System.out.println("京剧术语");
    }
}

public class Example {
    public static void main(String[] args) {
        ChinaPeople chinaPeople = new ChinaPeople();
        AmericanPeople americanPeople = new AmericanPeople();
        BeijingPeople beijingPeople = new BeijingPeople();

        chinaPeople.speakHello();
        americanPeople.speakHello();
        beijingPeople.speakHello();

        chinaPeople.averageHeight();
        americanPeople.averageHeight();
        beijingPeople.averageHeight();

        chinaPeople.averageWeight();
        americanPeople.averageWeight();
        beijingPeople.averageWeight();

        chinaPeople.chinaGongfu();
        americanPeople.americanBoxing();
        beijingPeople.beijingOpera();
        beijingPeople.chinaGongfu();
    }
}