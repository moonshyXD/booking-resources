class AccountEmailBuilder:
    def get_text_created_account(self, email: str, password: str) -> str:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; border: 1px solid #eaeaea; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h2 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px;">Добро пожаловать в систему бронирования общих ресурсов!</h2>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Ваш аккаунт был успешно создан. Теперь вы можете войти в систему, используя следующие данные:</p>
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; border-radius: 4px; margin: 20px 0;">
                <p style="margin: 0 0 10px 0; font-size: 15px;"><strong>Email (Логин):</strong> <a href="mailto:{email}" style="color: #3498db; text-decoration: none;">{email}</a></p>
                <p style="margin: 0; font-size: 15px;"><strong>Пароль:</strong> <span style="font-family: monospace; background: #e2e8f0; padding: 4px 8px; border-radius: 4px; color: #e74c3c;">{password}</span></p>
            </div>
            <p style="font-size: 14px; color: #888; text-align: center; margin-top: 30px;">Пожалуйста, сохраните это письмо с паролем для входа в систему.</p>
        </div>
        """

    def get_text_updated_password(self, email: str, new_password: str) -> str:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; border: 1px solid #eaeaea; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h2 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">Обновление пароля</h2>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Здравствуйте! Пароль от вашего аккаунта <strong>{email}</strong> был успешно изменен.</p>
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #f39c12; border-radius: 4px; margin: 20px 0;">
                <p style="margin: 0; font-size: 15px;"><strong>Ваш новый пароль:</strong> <span style="font-family: monospace; background: #e2e8f0; padding: 4px 8px; border-radius: 4px; color: #27ae60;">{new_password}</span></p>
            </div>
            <p style="font-size: 14px; color: #888; text-align: center; margin-top: 30px;">Если вы не запрашивали смену пароля, срочно свяжитесь с поддержкой.</p>
        </div>
        """

    def get_text_updated_account_data(self, email: str, password: str) -> str:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; border: 1px solid #eaeaea; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h2 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #27ae60; padding-bottom: 10px;">Данные профиля обновлены</h2>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Здравствуйте! Мы хотим сообщить, что личные данные в вашем аккаунте <strong>{email}</strong> были успешно изменены.</p>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Все новые настройки уже вступили в силу. Вы можете проверить актуальную информацию в своем личном кабинете. Новый пароль для аккаунта {password}</p>
            <p style="font-size: 14px; color: #888; text-align: center; margin-top: 30px;">Если эти изменения вносили не вы, пожалуйста, немедленно обратитесь в службу поддержки.</p>
        </div>
        """

    def get_text_deleted_account(self, email: str) -> str:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; border: 1px solid #eaeaea; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h2 style="color: #c0392b; text-align: center; border-bottom: 2px solid #c0392b; padding-bottom: 10px;">Прощайте!</h2>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Ваш аккаунт, привязанный к почте <strong>{email}</strong>, был безвозвратно удален из нашей системы.</p>
            <p style="font-size: 16px; color: #555; line-height: 1.5;">Все ваши персональные данные стерты. Нам очень жаль, что вы нас покидаете. Если решите вернуться, мы всегда будем рады видеть вас снова!</p>
        </div>
        """