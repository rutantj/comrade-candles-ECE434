#include<stdio.h>
#include<fcntl.h>
#include<unistd.h>
#include<termios.h>   // using the termios.h library

int main() {
   int file;
   file = open("/dev/ttyO1", O_RDWR | O_NOCTTY | O_NDELAY);

      struct termios options;               //The termios structure is vital
      tcgetattr(file, &options);            //Sets the parameters associated with file
      options.c_cflag = B9600 | CS8 | CREAD | CLOCAL;
      options.c_iflag = IGNPAR | ICRNL;    //ignore partity errors, CR -> newline
      tcflush(file, TCIFLUSH);             //discard file information not transmitted
      tcsetattr(file, TCSANOW, &options);  //changes occur immmediately

      unsigned char receive[100];  //the string to send
while(1) {
      int characters = read(file, (void*)receive,100);       //send the string
      if (characters == -1) {
          
      }
      receive[characters] = 0;
      sleep(2);
      printf("%s ", receive);
      fflush(stdout);

}
       return 0;
}

