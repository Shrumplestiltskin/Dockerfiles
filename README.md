https://gist.github.com/Shrumplestiltskin/a01c01c9cf64576aefab5011f0d81b9d

##Stuff  
#On disk container locations -  
/var/lib/docker/containers  #find configs here  
/proc/[container pid]/root

##Docker / Namespace CVEs
The deafult OCI linux spec in oci/defaults{_linux}.go in Docker/Moby  
from 1.11 to current upstream master does not block /proc/acpi pathnames  
allowing attackers to modify host's hardware like enabling/disabling  
bluetooth or turning up/down keyboard brightness and probably other stuff  
https://github.com/moby/moby/pull/37404  
