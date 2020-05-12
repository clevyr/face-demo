using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Services;


namespace FaceIdentifier
{
    public class EmployeeAndResult
    {
        const string FileDirectory = "../../data/faces";       
        public string Name { get; set; }
        public Image Image { get; set; }
        public Image FaceImage { get; set; }
        public IdentifyReply Reply { get; set; }
        public event Action OnGotReply;
        public bool Correct { get; set; }
        

        public static List<EmployeeAndResult> LoadEmployees()
        {
            var results = new List<EmployeeAndResult>();
            foreach (var filepath in Directory.EnumerateFiles(FileDirectory, "*-fun.jpg"))
            {
                var filename = Path.GetFileName(filepath);
                var splitResult = filename.Split("-");
                var name = String.Join('-', splitResult.Take(splitResult.Length - 1));
                var image = Image.FromFile(filepath);
                if (image != null)
                {
                    results.Add(new EmployeeAndResult
                    {
                        Name = name,
                        Image = image,
                    });                 
                   
                }

            }
            return results;
        }

        public byte[] GetImageData()
        {
            using (MemoryStream ms = new MemoryStream())
            {
                Image.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
                return ms.ToArray();
            }
        }

        public async Task GetResultAsync(Identifier.IdentifierClient client)
        {
            //recommended chunk size (64kb)
            var chunkSize = 64 * 1024;

            using var call = client.IdentifyImage();

            var imageData = GetImageData();

            var numChunks = Math.Ceiling(imageData.Length / (double)chunkSize);
            for (int i = 0; i < numChunks; ++i)
            {
                var count = numChunks == 1 ? Math.Min(imageData.Length, chunkSize) : Math.Min(chunkSize, (imageData.Length - (i * chunkSize)));
                var byteString = Google.Protobuf.ByteString.CopyFrom(imageData, i * chunkSize, count);
                var chunk = new IdentifyImageRequest { Image = byteString };
                await call.RequestStream.WriteAsync(chunk);
            }
            await call.RequestStream.CompleteAsync();

            Reply = await call;
            var first = Reply.Results.FirstOrDefault();
            if (first != null)
            {
                Correct = first.Nearest.Name == Name;
            }
            Console.WriteLine($"GOT REPLY!!! {this.Name}" );
            OnGotReply?.Invoke();
        }
    }


}
