using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;


namespace FaceIdentifier
{

    //public class FaceIdentifierClient : FaceIdentifierService.FaceIdentifier.FaceIdentifierClient
    //{       
    //    public FaceIdentifierClient(ChannelBase channel) : base(channel) { }

    //    public FaceIdentifierClient() : base(new GrpcChannel("127.0.0.1:5001", ChannelCredentials.Insecure))
    //    {
    //        Console.WriteLine("OH YEAH!");
    //    }

    //    public override IdentifyReply Identify(IdentifyRequest request, CallOptions options)
    //    {
    //        Console.WriteLine("TAG  IMAGE");
    //        return base.Identify(request, options);
    //    }
    //}


    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        // For more information on how to configure your application, visit https://go.microsoft.com/fwlink/?LinkID=398940
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddRazorPages();
            services.AddServerSideBlazor();


            AppContext.SetSwitch(
                "System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);
            services.AddGrpcClient<FaceIdentifierService.FaceIdentifier.FaceIdentifierClient>(o =>
            {
                o.Address = new Uri("http://127.0.0.1:5002");


            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseStaticFiles();

            app.UseRouting();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapBlazorHub();
                endpoints.MapFallbackToPage("/_Host");
            });
        }
    }
}
