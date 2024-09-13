using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace wwi_app.Controllers
{
    public partial class FrontEndController : Controller
    {
        [ResponseCache(Duration = 60)]
        public IActionResult Index() { return View(); }

        [ResponseCache(Duration = 60)]
        public IActionResult Offers() { return View(); }

        [ResponseCache(Duration = 60)]
        public IActionResult Contact() { return View(); }

        [Authorize]
        public IActionResult BuyingGroups() { return View(); }

        [Authorize]
        public IActionResult Cities() { return View(); }

        [Authorize]
        public IActionResult Colors() { return View(); }

        [Authorize]
        public IActionResult Countries() { return View(); }

        [Authorize]
        public IActionResult CustomerCategories() { return View(); }

        [Authorize]
        public IActionResult Customers() { return View(); }

        [Authorize]
        public IActionResult CustomerTransactions() { return View(); }

        [Authorize]
        public IActionResult Dashboard() { return View(); }

        [Authorize]
        public IActionResult Deals() { return View(); }

        [Authorize]
        public IActionResult DeliveryMethods() { return View(); }

        [Authorize]
        public IActionResult Invoices() { return View(); }

        [Authorize]
        public IActionResult PackageTypes() { return View(); }

        [Authorize]
        public IActionResult PaymentMethods() { return View(); }

        [Authorize]
        public IActionResult PurchaseOrders() { return View(); }

        [Authorize]
        public IActionResult SalesOrders() { return View(); }

        [Authorize]
        public IActionResult StateProvinces() { return View(); }

        [Authorize]
        public IActionResult StockGroups() { return View(); }

        [Authorize]
        public IActionResult StockItems() { return View(); }

        [Authorize]
        public IActionResult SupplierCategories() { return View(); }

        [Authorize]
        public IActionResult Suppliers() { return View(); }

        [Authorize]
        public IActionResult SupplierTransactions() { return View(); }

        [Authorize]
        public IActionResult TransactionTypes() { return View(); }
    }
}
