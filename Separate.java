public class Separate {
    public static void main(String[] args) {
        int[] arr = {1, 0, 1, 0, 1, 0, 0, 1};

        int count = 0;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == 0) {
                count++;
            }
        }

        for (int i = 0; i < count; i++) {
            arr[i] = 0;
        }
        for (int i = count; i < arr.length; i++) {
            arr[i] = 1;
        }

        System.out.println("Array after separating 0s and 1s:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
}
