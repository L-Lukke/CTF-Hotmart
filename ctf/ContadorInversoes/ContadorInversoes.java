public class ContadorInversoes {
    public static void main(String[] args) {
        int[] array = {53, 86, 45, 97, 93};
        int inversoes = contarInversoes(array);
        System.out.println("Número de inversões: " + inversoes);
    }

    public static int contarInversoes(int[] array) {
        int contagem = 0;
        int n = array.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (array[i] > array[j]) {
                    contagem++;
                }
            }
        }
        return contagem;
    }
}
