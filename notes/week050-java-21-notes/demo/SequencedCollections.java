import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class SequencedCollections {
    
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("a");
        list.add("b");
        list.add("c");
        list.add("d");
        test_old_list(list);
        test_new_list(list);

        Deque<String> deque = new ArrayDeque<>();
        deque.add("aa");
        deque.add("bb");
        deque.add("cc");
        deque.add("dd");
        test_old_deque(deque);
        test_new_deque(deque);
    }

    private static void test_old_list(List<String> list) {
        System.out.println("The first element is: " + list.get(0));
        System.out.println("The last element is: " + list.get(list.size() - 1));
        for (var it = list.listIterator(list.size()); it.hasPrevious();) {
            var e = it.previous();
            System.out.println(e);
        }
    }

    private static void test_new_list(List<String> list) {
        System.out.println("The first element is: " + list.getFirst());
        System.out.println("The last element is: " + list.getLast());
        list.reversed().forEach(it -> System.out.println(it));
    }

    private static void test_old_deque(Deque<String> deque) {
        System.out.println("The first element is: " + deque.getFirst());
        System.out.println("The last element is: " + deque.getLast());
        for (var it = deque.descendingIterator(); it.hasNext();) {
            var e = it.next();
            System.out.println(e);
        }
    }

    private static void test_new_deque(Deque<String> deque) {
        System.out.println("The first element is: " + deque.getFirst());
        System.out.println("The last element is: " + deque.getLast());
        deque.reversed().forEach(it -> System.out.println(it));
    }
}
