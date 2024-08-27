package solostudy.dfs;
import java.util.*;
import java.io.*;

public class 그림1926 {
    static int n,m,C;
    static int[][] b;
    static boolean[][] v;

    static final int[] di = {-1,0,1,0};
    static final int[] dj = {0,1,0,-1};

    static void dfs(int i,int j){
        v[i][j] = true;
        C++;
        for(int d=0;d<4;d++){
            int ni = i+di[d];
            int nj = j+dj[d];
            if(ni>=0 && nj>=0 && ni<n&& nj<m && !v[ni][nj] && b[ni][nj]==1){
                dfs(ni,nj);
            }
        }
    }

    public static void main(String[] args)throws Exception{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        st = new StringTokenizer(br.readLine()," ");
        n = Integer.parseInt(st.nextToken());
        m = Integer.parseInt(st.nextToken());
        b = new int[n][m];
        v = new boolean[n][m];

        for(int i=0;i<n;i++){
            st = new StringTokenizer(br.readLine()," ");
            for(int j=0;j<m;j++){
                b[i][j] = Integer.parseInt(st.nextToken());
            }
//            System.out.println(Arrays.toString(b[i]));
        }

        int sum =0;
        int max = 0;

        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(b[i][j] == 1 && !v[i][j]){
                    C =0;
                    dfs(i,j);
                    sum++;
                    max = Math.max(max,C);
                }
            }
        }
        System.out.println(sum);
        System.out.println(max);

    }
}
