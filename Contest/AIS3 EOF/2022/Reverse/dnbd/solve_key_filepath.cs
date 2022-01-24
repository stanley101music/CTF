using System;
using System.Text;
using System.Linq;


public class Program
{
    public static uint PrintByteArray(byte[] bytes)
    {
        var sb = new StringBuilder("new byte[] { ");
        foreach (var b in bytes)
        {
            sb.Append(b + ", ");
        }
        sb.Append("}");
        Console.WriteLine(sb.ToString());
        return 0;
    }

    public static void Main()
    {
        int num = 36;
        byte[] bytes = {0x69, 0x54, 0x41, 0x56, 0x67, 0x58, 0x4c, 0x64, 0x57, 0x41, 0x6b, 0x78, 0x53, 0x4c, 0x35, 0x61, 0x45, 0x69, 0x69, 0x57, 0x79, 0x5a, 0x71, 0x54, 0x61, 0x6a, 0x31, 0x35, 0x42, 0x48, 0x5a, 0x5a};
        byte[] array = {0x71,0x59,0x6a,0x6d,0x16,0x53,0x10,0x16,0x3f,0x40,0x42,0x38,0x75,0x5d,0x01,0x42,0x0c,0x04,0x5c,0x16,0x12,0x6b,0x4d,0x17,0x05,0x5a,0x17,0x56,0x4a,0x5b,0x47,0x45,0x1c,0x17,0x4e,0x4c};
        string s2 = CCC.Calculate(bytes);
        byte[] bytes2 = Encoding.ASCII.GetBytes(s2);
        int num2 = bytes2.Length;
        PrintByteArray(bytes2);
        for (int i = 0; i < num; i++)
        {
            array[i] ^= bytes2[i % num2];
        }
        string filename = Encoding.UTF8.GetString(array).TrimEnd(new char[1]);
        Console.WriteLine(filename);
    }
}

// Token: 0x02000002 RID: 2
public static class CCC
{
    // Token: 0x06000001 RID: 1 RVA: 0x00002048 File Offset: 0x00000248
    public static uint leftRotate(uint x, int c)
    {
        return x << c | x >> 32 - c;
    }

    // Token: 0x06000002 RID: 2 RVA: 0x0000205C File Offset: 0x0000025C
    public static string Calculate(byte[] input)
    {
        uint num = 1732584193U;
        uint num2 = 4023233417U;
        uint num3 = 2562383102U;
        uint num4 = 271733878U;
        int num5 = (56 - (input.Length + 1) % 64) % 64;
        byte[] array = new byte[input.Length + 1 + num5 + 8];
        Array.Copy(input, array, input.Length);
        array[input.Length] = 128;
        Array.Copy(BitConverter.GetBytes(input.Length * 8), 0, array, array.Length - 8, 4);
        for (int i = 0; i < array.Length / 64; i++)
        {
            uint[] array2 = new uint[16];
            for (int j = 0; j < 16; j++)
            {
                array2[j] = BitConverter.ToUInt32(array, i * 64 + j * 4);
            }
            uint num6 = num;
            uint num7 = num2;
            uint num8 = num3;
            uint num9 = num4;
            uint num10 = 0U;
            uint num11 = 0U;
            for (uint num12 = 0U; num12 < 64U; num12 += 1U)
            {
                if (num12 <= 15U)
                {
                    num10 = ((num7 & num8) | (~num7 & num9));
                    num11 = num12;
                }
                else if (num12 >= 16U && num12 <= 31U)
                {
                    num10 = ((num9 & num7) | (~num9 & num8));
                    num11 = (5U * num12 + 1U) % 16U;
                }
                else if (num12 >= 32U && num12 <= 47U)
                {
                    num10 = (num7 ^ num8 ^ num9);
                    num11 = (3U * num12 + 5U) % 16U;
                }
                else if (num12 >= 48U)
                {
                    num10 = (num8 ^ (num7 | ~num9));
                    num11 = 7U * num12 % 16U;
                }
                uint num13 = num9;
                num9 = num8;
                num8 = num7;
                num7 += CCC.leftRotate(num6 + num10 + CCC.K[(int)num12] + array2[(int)num11], CCC.s[(int)num12]);
                num6 = num13;
            }
            num += num6;
            num2 += num7;
            num3 += num8;
            num4 += num9;
        }
        return CCC.GetByteString(num) + CCC.GetByteString(num2) + CCC.GetByteString(num3) + CCC.GetByteString(num4);
    }

    // Token: 0x06000003 RID: 3 RVA: 0x00002227 File Offset: 0x00000427
    private static string GetByteString(uint x)
    {
        return string.Join("", from y in BitConverter.GetBytes(x)
                           select y.ToString("x2"));
    }

    // Token: 0x04000001 RID: 1
    private static int[] s = new int[]
    {
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21
    };

    // Token: 0x04000002 RID: 2
    private static uint[] K = new uint[]
    {
        3614090360U,
        3905402710U,
        606105819U,
        3250441966U,
        4118548399U,
        1200080426U,
        2821735955U,
        4249261313U,
        1770035416U,
        2336552879U,
        4294925233U,
        2304563134U,
        1804603682U,
        4254626195U,
        2792965006U,
        1236535329U,
        4129170786U,
        3225465664U,
        643717713U,
        3921069994U,
        3593408605U,
        38016083U,
        3634488961U,
        3889429448U,
        568446438U,
        3275163606U,
        4107603335U,
        1163531501U,
        2850285829U,
        4243563512U,
        1735328473U,
        2368359562U,
        4294588738U,
        2272392833U,
        1839030562U,
        4259657740U,
        2763975236U,
        1272893353U,
        4139469664U,
        3200236656U,
        681279174U,
        3936430074U,
        3572445317U,
        76029189U,
        3654602809U,
        3873151461U,
        530742520U,
        3299628645U,
        4096336452U,
        1126891415U,
        2878612391U,
        4237533241U,
        1700485571U,
        2399980690U,
        4293915773U,
        2240044497U,
        1873313359U,
        4264355552U,
        2734768916U,
        1309151649U,
        4149444226U,
        3174756917U,
        718787259U,
        3951481745U
    };
}