using Microsoft.AspNet.Cryptography.KeyDerivation;
using System;
using System.Linq;

namespace pbkdf2
{
    class Program
    {
        /// <summary>
        /// Main method
        /// </summary>
        static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                PrintUsage();
                System.Environment.Exit(1);
            }

            string password = args[0];
            string hexSalt = args[1];

            byte[] salt = StringToByteArray(hexSalt);
            Console.WriteLine(GetHashedPassword(password, salt));
        }

        /// <summary>
        /// Convert hex string to byte array
        /// </summary>
        /// <param name="hex">Hexadecimal string</param>
        /// <returns>Byte array representation of the string</returns>
        private static byte[] StringToByteArray(string hex) => Enumerable.Range(0, hex.Length)
                .Where(x => x % 2 == 0)
                .Select(x => Convert.ToByte(hex.Substring(x, 2), 16))
                .ToArray();

        /// <summary>
        /// Generate hashed password with the given salt
        /// </summary>
        /// <param name="password">Password to be hashed</param>
        /// <param name="salt">Byte array of salt</param>
        /// <returns>Hashed and salted password</returns>
        private static string GetHashedPassword(String password, byte[] salt)
        {
            // Derive a 32 bytes subkey (use HMACSHA1 with 10,000 iterations)
            //
            return Convert.ToBase64String(KeyDerivation.Pbkdf2(
                password: password,
                salt: salt,
                prf: KeyDerivationPrf.HMACSHA1,
                iterationCount: 10000,
                numBytesRequested: 32));
        }

        /// <summary>
        /// Prints usage of the program
        /// </summary>
        private static void PrintUsage()
        {
            Console.WriteLine("Usage:");
            Console.WriteLine("pbkdf2 <password> <hex salt>");
        }
    }
}
