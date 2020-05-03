USE ecommercedb;

#Address
INSERT INTO `address`(`id`, `id_user`, `owner`, `phone_number`, `no`, `street`, `ward`, `district`, `city`, `created_date`, `delete_date`)
VALUES(1, 1 ,"Chủ chợ sách", "0000111100", "273", "An Dương Vương", "5", "3", "Hồ Chí Minh", "2020-04-25 04:04:27", null);

#Merchandise portfolio
INSERT INTO `merchandise_portfolio`(`id`, `code`, `name`, `created_date`, `created_by`, `delete_date`)
VALUES(1, "book", "Sách", "2020-04-25 04:04:27", 1, null);

#Merchandise condition
INSERT INTO `merchandise_condition`(`id`, `code`, `name`, `created_date`, `created_by`, `delete_date`)
VALUES(1, "new", "Mới", "2020-04-25 04:04:27", 1, null);
INSERT INTO `merchandise_condition`(`id`, `code`, `name`, `created_date`, `created_by`, `delete_date`)
VALUES(2, "used", "Đã sử dụng", "2020-04-25 04:04:27", 1, null);

#Store
INSERT INTO `store`(`id_user`, `name`, `avatar_url`, `description`, `phone_number`)
VALUES(1, "Chợ Sách Store", "https://media.gettyimages.com/photos/stack-of-books-picture-id157482029?s=612x612", "Cửa hàng sách uy tín của Chợ Sách. Đảm bảo mang lại những sản phẩm chất lượng, chính hãng.", "0123123123");