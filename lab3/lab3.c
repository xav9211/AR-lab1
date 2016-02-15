#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>

int rank;
int world_size;

int main(int argc, char** argv) {
	MPI_Init(NULL, NULL);

	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);

	if (rank == world_size - 1) {
		double MPI_Wtime();
		

	}


	MPI_Finalize();
}