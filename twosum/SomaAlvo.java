import java.util.HashMap;
import java.util.Map;

public class SomaAlvo {
    public static void main(String[] args) {
        int[] array = {17, 6, 8, 69, 91, 50, 31, 78, 85, 83, 26, 96, 57, 98, 32, 41, 34, 33, 81, 42, 54, 94, 53, 37, 47, 19, 62, 43, 71, 97, 60, 49, 1, 30, 68, 25, 23, 52, 74, 4};
        int target = 56;
        
        int[] resultado = encontrarPar(array, target);
        
        if (resultado.length == 0) {
            System.out.println("Nenhum par de números soma o alvo.");
        } else {
            System.out.println("Os números que somam " + target + " são: " + resultado[0] + " e " + resultado[1]);
        }
    }

    public static int[] encontrarPar(int[] nums, int target) {
        Map<Integer, Integer> mapa = new HashMap<>();
        
        for (int num : nums) {
            int complemento = target - num;
            if (mapa.containsKey(complemento)) {
                return new int[]{complemento, num};
            }
            mapa.put(num, 1);
        }
        
        return new int[]{};
    }
}
