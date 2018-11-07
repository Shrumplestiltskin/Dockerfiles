#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
int main(void){
	FILE *out_file = fopen("/etc/resolv.conf", "a");

	if ( out_file == NULL )
	{
		printf("Error! Could not open file\n");
		exit(-1);
	}

	fprintf(out_file, "EXPLOITED LEEEL");
	fclose(out_file);
	for (;;) pause();
	return 0;
}
