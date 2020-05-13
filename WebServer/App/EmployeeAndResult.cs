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
        private static List<EmployeeAndResult> _Employees { get; set; }
        public static List<EmployeeAndResult> Employees
        {
            get
            {
                return CheckUpdateEmployees();
            }
            private set { _Employees = value; }
        }
        public string Name { get; set; }
        public Byte[] ImageBytes { get; set; }        
        public IdentifyReply Reply { get; set; }
        public event Action OnGotReply;
        public bool Correct { get; set; }


        static EmployeeAndResult()
        {
            Employees = ForceLoadEmployees();
        }

        public static List<EmployeeAndResult> ForceLoadEmployees()
        {
            var results = new List<EmployeeAndResult>();
            foreach (var filepath in Directory.EnumerateFiles(FileDirectory, "*-fun.jpg"))
            {
                var filename = Path.GetFileName(filepath);
                var splitResult = filename.Split("-");
                var name = String.Join('-', splitResult.Take(splitResult.Length - 1));
                //var image = Image.FromFile(filepath);
                var imageStream = File.OpenRead(filepath);
                if (imageStream != null)
                {
                    var bytes = new byte[imageStream.Length];
                    imageStream.Read(bytes, 0, (int)imageStream.Length);
                    results.Add(new EmployeeAndResult
                    {
                        Name = name,
                        ImageBytes = bytes,
                    });

                }

            }
            _Employees = results;
            return results;
        }

        private static List<EmployeeAndResult> CheckUpdateEmployees()
        {
            var employeeImages = Directory.EnumerateFiles(FileDirectory, "*-fun.jpg").ToList();
            if (_Employees.Count != employeeImages.Count)
            {
                return ForceLoadEmployees();
            }
            else
            {
                var employeeNames = _Employees.Select(x => x.Name).ToHashSet();
                var fileEmployeeNames = employeeImages.Select(filepath =>
                {
                    var filename = Path.GetFileName(filepath);
                    var splitResult = filename.Split("-");
                    return String.Join('-', splitResult.Take(splitResult.Length - 1));
                }).ToHashSet();

                employeeNames.SymmetricExceptWith(fileEmployeeNames);
                if (employeeNames.Any())
                {
                    return ForceLoadEmployees();
                }
            }
            return _Employees;
        }
        

        public async Task GetResultAsync(Identifier.IdentifierClient client)
        {
            //recommended chunk size (64kb)
            var chunkSize = 64 * 1024;

            using var call = client.IdentifyImage();
            

            var numChunks = Math.Ceiling(ImageBytes.Length / (double)chunkSize);
            for (int i = 0; i < numChunks; ++i)
            {
                var count = numChunks == 1 ? Math.Min(ImageBytes.Length, chunkSize) : Math.Min(chunkSize, (ImageBytes.Length - (i * chunkSize)));
                var byteString = Google.Protobuf.ByteString.CopyFrom(ImageBytes, i * chunkSize, count);
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
            Console.WriteLine($"GOT REPLY!!! {this.Name}");
            OnGotReply?.Invoke();
        }
    }


}
