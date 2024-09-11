import java.util.ArrayList;
import java.util.List;

public class ReorganizeList {

    public static List<Integer> reorganizeList(List<Integer> nums) {
        List<Integer> pares = new ArrayList<>();
        List<Integer> impares = new ArrayList<>();

        for (Integer num : nums) {
            if (num % 2 == 0) {
                pares.add(num);
            } else {
                impares.add(num);
            }
        }

        List<Integer> resultado = new ArrayList<>(pares);
        resultado.addAll(impares);
        return resultado;
    }

    public static void main(String[] args) {
        List<Integer> lista = List.of(-24, 51, 78, -92, -92, -17, 92, -38, 54, -87, -7, -49, 39, 2, -9, -1, -72, 40, -68, -54);
        List<Integer> resultado = reorganizeList(lista);
        System.out.println(resultado);
    }
    
}
