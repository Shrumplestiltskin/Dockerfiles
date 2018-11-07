Displays some concepts.  

https://github.com/opencontainers/runc/blob/master/libcontainer/SPEC.md  
Even when a FROM scratch image is created with a static binary runtime files are created -  
/etc/hosts  
/etc/resolv.conf  
/etc/hostname  
/etc/localtime  

These can be viewed by grabbing pid and viewing files in proc -  
#docker run --rm --name file-write file-write  
#docker inspect -f {{.State.Pid}} [container-name]  
#cd /proc/[container_pid]/root  
#ls -alh  

Another concept shown here is the CoW - 
https://docs.docker.com/storage/storagedriver/#the-copy-on-write-cow-strategy  

resolv.conf is only modified in the container. This is only possible because we are running as 0 pid.  

If you run the container with non-zero pid the application will return per prog.  
#docker run --rm -u 1234 --name file-write file-write  
Error! Could not open file  
#echo $?  
255  



Good ref -  
https://embano1.github.io/post/scratch/  
