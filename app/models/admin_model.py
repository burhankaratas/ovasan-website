from app.utils.logs import save_error
from app.extensions import mysql

class Contact:
    """
    Bu sınıf site üzerinden gelen mesajlar için veritabanı işlemlerini kapsar.
    """

    def __init__(self):
        self.db = mysql

    def create(self, company_name, name, email, phone, service, message):
        """
        Yeni mesaj ekler.
        """
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "INSERT INTO contact (company_name, name, email, phone, service, message) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (company_name, name, email, phone, service, message))

            if cursor.rowcount > 0:
                self.db.connection.commit()

                return True, "Mesaj başarıyla gönderildi."
            

            return False, "Mesajınız gönderilemedi. Lütfen tekrar deneyiniz."

        except Exception as e:
            save_error(f"Contact.create: {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."

        finally:
            if cursor:
                cursor.close()

    def get_all(self, page=1, per_page=5):
        """
        Sayfalamalı olarak mesajları listeler.
        page: kaçıncı sayfa
        per_page: sayfa başına mesaj sayısı
        """
        cursor = None
        try:
            offset = (page - 1) * per_page
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM contact ORDER BY created_date DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (per_page, offset))

            datas = cursor.fetchall()
            return datas

        except Exception as e:
            save_error(f"Contact.get_all: {str(e)}")
            return []

        finally:
            if cursor:
                cursor.close()

    def count(self):
        """
        Toplam mesaj sayısını döner (sayfalama için kullanılacak).
        """
        cursor = None
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT COUNT(*) AS total FROM contact"
            cursor.execute(query)
            result = cursor.fetchone()
            total = result["total"] if result else 0
            return total
    
        except Exception as e:
            save_error(f"Contact.count: {str(e)}")
            return 0
    
        finally:
            if cursor:
                cursor.close()
    
    
class Categories:
    """
    Bu sınıf projeler ve servislerin kategorilerinin eklenmesi, düzenlenmesi 
    ve güncellenmesi için gerekli CRUD işlemlerini kapsar.
    """

    def __init__(self):
        self.db = mysql

    def check_slug(self, slug):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT slug FROM categories WHERE slug = %s"
            result = cursor.execute(query, (slug,))

            if result > 0:
                return True
            
            return False

        except Exception as e:
            save_error(f"Categories.check_slug(): {str(e)}")
            return False
        
        finally:
            if cursor:
                cursor.close()

    def create(self, name, slug, category_type, image_url):
        cursor = None
        try:
            status = Categories.check_slug(self, slug)

            if status:
                return False, "Slug zaten başka biryerde kullanılmış."

            cursor = self.db.connection.cursor()

            query = "INSERT INTO categories (name, slug, category_type, image) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, slug, category_type, image_url))

            if cursor.rowcount > 0:
                self.db.connection.commit()
                return True, "Kategori oluşturuldu."
            
            return False, "Kategori oluşturulamadı."

        except Exception as e:
            save_error(f"Categories.create(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()


    def edit(self, name, slug, category_type, category_id):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "UPDATE categories SET name = %s, slug = %s, category_type = %s WHERE id = %s"
            cursor.execute(query, (name, slug, category_type, category_id))

            if cursor.rowcount > 0:
                self.db.connection.commit()
                return True, "Kategori güncellendi."
            
            return False, "Kategori güncellenemedi."

        except Exception as e:
            save_error(f"Categories.edit(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()
    
    def delete(self, category_id):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "DELETE FROM categories WHERE id = %s"
            cursor.execute(query, (category_id,))

            if cursor.rowcount > 0:
                self.db.connection.commit()
                return True, "Kategori silindi."

        except Exception as e:
            save_error(f"Categories.delete(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()

    def get_all(self):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM categories ORDER BY id DESC"
            result = cursor.execute(query)

            if result > 0:
                datas = cursor.fetchall()
                return True, datas
            
            return True, []

        except Exception as e:
            save_error(f"Categories.get_all(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()

    def get(self, category_id):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM categories WHERE id = %s"
            result = cursor.execute(query, (category_id,))

            if result > 0:
                data = cursor.fetchone()
                return True, data
            
            return False, "Kategori bulunamadı."

        except Exception as e:
            save_error(f"Categories.get_all(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()

    def get_id_by_slug(self, slug):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT id FROM categories WHERE slug = %s"
            result = cursor.execute(query, (slug,))

            if result > 0:
                data = cursor.fetchone()

                return True, data["id"]
            
            return False, "Böyle bir kategori bulunmamaktadır."

        except Exception as e:
            save_error(f"Services.get_id_by_slug(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()

    
    def get_all_by_type(self, category_type):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM categories WHERE category_type = %s"
            result = cursor.execute(query, (category_type,))

            if result > 0:
                datas = cursor.fetchall()
                return True, datas
            
            return True, []

        except Exception as e:
            save_error(f"Categories.get_all_by_type(): {str(e)}")
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz."
        
        finally:
            if cursor:
                cursor.close()


class Services:
    """
    Bu sınıf hizmetler sayfalarını oluşturmak, güncellemek, silmek gibi 
    temel CRUD işlemlerini içerir.
    """

    def __init__(self):
        self.db = mysql


    def create(self, data):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = """
            INSERT INTO services 
            (category_id, title, slug, main_heading, subtitle1, subtitle2, subtitle3, subtitle4,
            text1, text2, text3, text4, text5, text6, text7, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data.get("category_id"),
                data.get("title"),
                data.get("slug"),
                data.get("main_heading"),
                data.get("subtitle1"),
                data.get("subtitle2"),
                data.get("subtitle3"),
                data.get("subtitle4"),
                data.get("text1"),
                data.get("text2"),
                data.get("text3"),
                data.get("text4"),
                data.get("text5"),
                data.get("text6"),
                data.get("text7"),
                data.get("image")
            ))

            if cursor.rowcount > 0:
                self.db.connection.commit()
                return True, "Hizmet oluşturuldu."

            return False, "Hizmet oluşturulamadı."

        except Exception as e:
            save_error(f"Services.create(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()

    def delete(self, service_id):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "DELETE FROM services WHERE id = %s"
            cursor.execute(query, (service_id,))

            if cursor.rowcount > 0:
                self.db.connection.commit()

                return True, "Hizmet silindi."
            
            return False, "Hizmet silinemedi."

        except Exception as e:
            save_error(f"Services.delete(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()

    def get_all(self):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM services ORDER BY id DESC"
            result = cursor.execute(query)

            if result > 0:
                datas = cursor.fetchall()
                return True, datas
            
            return True, []

        except Exception as e:
            save_error(f"Services.get_all(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()

    def get_by_slug(self, slug):
        cursor = None
        try:
            cursor = self.db.connection.cursor()

            query = "SELECT * FROM services WHERE slug = %s"
            result = cursor.execute(query, (slug,))

            if result > 0:
                datas = cursor.fetchone()

                return True, datas
            
            return False, "Böyle bir hizmetimiz bulunmamaktadır."

        except Exception as e:
            save_error(f"Services.get_by_slug(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()


    def get_all_by_category_id(self, category_id):
        cursor = None
        try:
            cursor = mysql.connection.cursor()

            query = "SELECT * FROM services WHERE category_id = %s"
            result = cursor.execute(query, (category_id,))

            if result > 0:
                datas = cursor.fetchall()

                return True, datas
            
            return True, []

        except Exception as e:
            save_error(f"Services.get_all_by_category_id(): {str(e)}")
            return False, "Beklenmedik bir hata oluştu."

        finally:
            if cursor:
                cursor.close()