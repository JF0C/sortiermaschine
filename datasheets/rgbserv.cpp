#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <wiringPi.h>

const int out = 0, oe = 1, s0 = 2, s1 = 3, s2 = 4, s3 = 5, servo = 12; //Pinbelegung
int rgb[4];

int setup()
{
        if(wiringPiSetup() == -1) return 0;

        pinMode(out, INPUT);
        pinMode(oe, OUTPUT);
        pinMode(s0, OUTPUT);
        pinMode(s1, OUTPUT);
        pinMode(s2, OUTPUT);
        pinMode(s3, OUTPUT);
        pinMode(servo, OUTPUT);

        return 1;
}

void rgbsens()
{
        time_t start;
        int change = 0, mesureinterval = 100000;
        for(int i=0; i<4; i++)
        {
                rgb[i] = 0;
        }

        //set frequency to 2%
        digitalWrite(s0, 0);
        digitalWrite(s1, 1);

        //set color filter to "no filter" => white
        digitalWrite(s2, 1);
        digitalWrite(s3, 0);

        start = clock();
        digitalWrite(oe, 1);

        //count output periods
        while(clock() - start < mesureinterval)
        {
                if(digitalRead(out) && !change)
                {
                        change = 1;
                        rgb[0] ++;
                }
                else if(!digitalRead(out) && change)
                {
                        change = 0;
                }
        }

        digitalWrite(oe, 0);
        change = 0;

        //set color filter to red
        digitalWrite(s2, 0);
        digitalWrite(s3, 0);

        start = clock();
        digitalWrite(oe, 1);
        while(clock() - start < mesureinterval)
        {
                if(digitalRead(out) && !change)
                {
                        change = 1;
                        rgb[1] ++;
                }
                else if(!digitalRead(out) && change)
                {
                        change = 0;
                }
        }

        digitalWrite(oe, 0);
        change = 0;

        //set color filter to blue
        digitalWrite(s2, 0);
        digitalWrite(s3, 1);

        start = clock();
        digitalWrite(oe, 1);
        while(clock() - start < mesureinterval)
        {
                if(digitalRead(out) && !change)
                {
                        change = 1;
                        rgb[3] ++;
                }
                else if(!digitalRead(out) && change)
                                {
                        change = 0;
                }
        }

        digitalWrite(oe, 0);
        change = 0;

        //set color filter to green
        digitalWrite(s2, 1);
        digitalWrite(s3, 1);

        start = clock();
        digitalWrite(oe, 1);
        while(clock() - start < mesureinterval)
        {
                if(digitalRead(out) && !change)
                {
                        change = 1;
                        rgb[2] ++;
                }
                else if(!digitalRead(out) && change)
                {
                        change = 0;
                }
        }

        digitalWrite(oe, 0);
}

void servoout(int degrees)
{

}

int main()
{
        setup();
        rgbsens();

        printf("\n\n\twhite = %i\n\n\tred = %i\n\n\tgreen = %i\n\n\tblue = %i\n\n", rgb[0], rgb[1], rgb[2], rgb[3]);

        return 0;
}
