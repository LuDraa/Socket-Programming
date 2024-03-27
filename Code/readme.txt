Note 1:
For grpc we have 2 server codes, one is for transferring the 10MB file (grpc_server10MB) and the other (server_grpc) is for sending rest of the files. two different files are created because the 10MB file is sent only 1 time hence the standard deviation (spread from the mean) is supposed to be 0 (there is only 1 value and it is the mean). The main code (server_grpc) could not support that hence we had to use a different code (grpc_server10MB) with another library statistics. 

Note 2:
For HTTP 1.1 and HTTP 2 we have implemented automation (the code asks for the file to sent at run-time) but for GRPC and Bittorent we couldn't do automation( the filename requested has to be changed in the code itself). This is the reason for having a seperate folder for grpc client, bittorent server and bittorent client.

Note 3:
For BitTorrent, the file bitserver implies the code for the peer which has the file and the file bitclient implies the code for other peers who are to download the file in a par-to-peer network.

Note 4:
The rest of the codes can be simply run on any ide (we used visual studio code) with python installed, the neccesarry libraries and how to install them is mentioned in the report file under section 2(libraries). For Bittorent the libraries will only be supported in MAC os having python version 3.9.

