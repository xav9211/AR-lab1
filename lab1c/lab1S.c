#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

double f(int x, int y){
	return 0.0;
}

void update_value(int x, int y, double **matrix, double above, double bellow){
	double left = matrix[x-1][y];
	double right = matrix[x+1][y];	
	double dt = 0.05;
	double new_value = ((above + bellow + right + left - 4*matrix[x][y] + f(x, y)) * dt) / 4.0;
	matrix[x][y] += new_value;	
}

int main (int argc, char * argv[])
{
	
	if (argc < 4)
	{
		printf("UŻYCIE: size, iteration_no\n");
		return(1);
	}
	
	int sizeM = atoi(argv[1]);
	int iteration_no = atoi(argv[2]);
	float temp = atof(argv[3]);

	// printf("RANK: %d, WORLD: %d", rank, size);

	// allocate own matrix
	double **matrix = (double **)malloc(sizeM * sizeof(double*));	
	int x,y;
	for(x = 0; x < sizeM; x++){
		matrix[x] = (double *)malloc(sizeM * sizeof(double));
	}
	
	for (x = 0; x < sizeM; x++){
		for(y = 0; y < sizeM; y++){
			matrix[x][y] = 0.0;
		}
	}

	//set temperature
	for (x=0; x < sizeM; x++){
		matrix[x][0] = temp;
	}
	
	struct timeval  start_time, end_time;
	gettimeofday(&start_time, NULL); 

	int i;
	for(i = 0; i < iteration_no; i++){		


		for (y = 1; y < sizeM - 1; y++){
			for (x = 1; x < sizeM-1; x++){
				update_value(x, y, matrix, matrix[x][y-1], matrix[x][y+1]);
			}
		}

	}

	gettimeofday(&end_time, NULL);
	double s_time = (start_time.tv_sec) * 1000 + (start_time.tv_usec) / 1000;
	double e_time = (end_time.tv_sec) * 1000 + (end_time.tv_usec) / 1000;
	double total_time = e_time - s_time;  
	printf("%F\n", total_time);
	//printf("X = %d, Y = %d, SIZE = %d, ITERATION_NO = %d, TOTAL_TIME = %d\n\n", sizeM, size, iteration_no, (int)total_time);		
	//printf("MACIERZ:\n");
	
 //  	for (i = 0; i < size; i++){
	// 	MPI_Barrier(MPI_COMM_WORLD);
	// 	if (rank == i){
	// 		for (y = 0; y < part_size_y; y++){
	// 			printf("[");
	// 			for(x = 0; x < sizeM; x++){
	// 				printf("%.2f ", matrix[x][y]);
	// 			}
	// 			printf("]\n");
	// 		}

	// 	}
	// }

	return 0;
}	