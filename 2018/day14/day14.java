import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.Collectors;

/*
LinkedList cannot be iterated while having elements added to it (why?!?), so
we implement the needed functionality directly, as a singly linked list with
a helper pointer to optimise fetching the last few elements of the list.

To run this: javac day14.java && java day14
*/

class Recipe {
    int value;
    Recipe next;

    Recipe(int recipe_value) {
        value = recipe_value;
        next = null;
    }
}

class Recipes {
    Recipe first = new Recipe(3);
    Recipe last = new Recipe(7);
    Recipe elf[] = new Recipe[2];
    Recipe seventeenth_from_end = null;
    int length = 2;

    Recipes() {
        first.next = last;
        elf[0] = first;
        elf[1] = last;
    }

    public int move_elf(int which) {
        int result = elf[which].value;
        for (int step = 0; step <= result; step++) {
            elf[which] = elf[which].next;
            if (elf[which] == null)
                elf[which] = first;
        }
        return result;
    }

    public int add(int value) {
        if (value > 9) {
            add(value / 10);
            return add(value % 10);
        }

        Recipe new_recipe = new Recipe(value);
        last.next = new_recipe;
        last = new_recipe;
        length++;

        if (length == 17)
            seventeenth_from_end = first;
        else if (length > 17)
            seventeenth_from_end = seventeenth_from_end.next;

        return length;
    }

    public void print() {
        for (Recipe current = first; current != null; current = current.next)
            if (elf[0] == current)
                System.out.print("(" + current.value + ")");
            else if (elf[1] == current)
                System.out.print("[" + current.value + "]");
            else
                System.out.print(" " + current.value + " ");
        System.out.println();
    }

    public int step() {
        int result = add(elf[0].value + elf[1].value);
        move_elf(0);
        move_elf(1);
        // print();
        return result;
    }

    public int[] last_few(int from) {
        return last_few(from, length - from);
    }

    public int[] last_few(int from, int how_many) {
        Recipe current;
        int f;
        if (seventeenth_from_end == null) {
            current = first;
            f = 0;
        } else {
            current = seventeenth_from_end;
            f = length - 17;
        }
        for (int i = f; i < from; i++)
            current = current.next;

        int result[] = new int[how_many];
        for (int i = 0; i < how_many; i++) {
            result[i] = current.value;
            current = current.next;
        }

        return result;
    }
}

public class day14 {
    public static String part1(String input) {
        int recipes_num = Integer.parseInt(input);
        int limit = recipes_num + 10;
        Recipes recipes = new Recipes();
        while (recipes.step() < limit);
        return Arrays.stream(recipes.last_few(recipes_num, 10))
            .mapToObj(String::valueOf)
            .collect(Collectors.joining(""));
    }

    public static int part2(String input) {
        char input_array[] = input.toCharArray();
        int input_len = input_array.length;
        int compare_to[] = new int[input_len];
        for (int i = 0; i < input_len; i++) {
            compare_to[i] = Character.getNumericValue(input_array[i]);
        }
        Recipes recipes = new Recipes();
        int first_unchecked = 0;

        while (true) {
            recipes.step();
            if (recipes.length >= input_len) {
                int last_few[] = recipes.last_few(first_unchecked);
                int last_first = last_few.length - input_len;
                int first;
                for (first = 0; first <= last_first; first++) {
                    int last = first + input_len - 1;
                    boolean ok = true;
                    for (int i = first; i <= last; i++) {
                        if (last_few[i] != compare_to[i - first]) {
                            ok = false;
                            break;
                        }
                    }
                    if (ok) return first_unchecked + first;
                }
                first_unchecked += last_first + 1;
            }
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        System.out.println("Test 1a: " + part1("9"));
        System.out.println("Test 1b: " + part1("5"));
        System.out.println("Test 1c: " + part1("18"));
        System.out.println("Test 1d: " + part1("2018"));

        System.out.println();

        System.out.println("Test 2a: " + part2("51589"));
        System.out.println("Test 2b: " + part2("01245"));
        System.out.println("Test 2c: " + part2("92510"));
        System.out.println("Test 2d: " + part2("59414"));

        System.out.println();

        Scanner sc = new Scanner(new File("day14.in"));
        String input = sc.nextLine();
        System.out.println(
            "Part 1 for input \"" + input + "\": " + part1(input)
        );
        System.out.println(
            "Part 2 for input \"" + input + "\": " + part2(input)
        );
    }
}
