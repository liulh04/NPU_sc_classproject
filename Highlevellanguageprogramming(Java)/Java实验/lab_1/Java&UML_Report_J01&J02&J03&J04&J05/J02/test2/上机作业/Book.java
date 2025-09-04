public class Book {
    private String title;
    private String pDate;
    private int words;

    public Book(String title, String pDate, int words) {
        this.title = title;
        this.pDate = pDate;
        this.words = words;
    }

    public double price() {
        double dateCoefficient;
        if (pDate.startsWith("First half")) {
            dateCoefficient = 1.2;
        } else {
            dateCoefficient = 1.18;
        }
        return words / 1000.0 * 35 * dateCoefficient;
    }

    public static void main(String[] args) {
        Book book = new Book("Java Programming", "First half of 2022", 50000);
        System.out.println("Title: " + book.title);
        System.out.println("Publication Date: " + book.pDate);
        System.out.println("Words: " + book.words);
        System.out.println("Price: " + book.price());
    }
}