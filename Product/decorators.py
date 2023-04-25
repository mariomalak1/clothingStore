def is_user_branch_is_this_branch(func):
    def check_it():
        pass


def current_user_is_admin(func):
    def checkit():
        try:
            user_ = User.query.filter_by(id = current_user.id).first()
        except:
            flash("انت لم تسجل بعد", "warning")
            return redirect(url_for("user.login"))
        else:
            if user_:
                if user_.IsAdmin():
                    return func()
                else:
                    n = Notification(notification_name=f"""لقد حاول المستخدم {user_.name} الدخول الي الصفحات المخصصة للمسؤل فقد و النظام منعه""", user_id = current_user.id)
                    db.session.add(n)
                    db.session.commit()
                    flash("انت لست مسؤل", "warning")
                    return redirect(url_for("user.login"))
            else:
                n = Notification(notification_name=f"""شخص ما غير مسجل علي النظام حاول الدخول للصفحات المخصصة للمسؤل فقد و لكن تم حذره من قبل النظام 
                اذا تكرر الامر برجاء مكالمة الصيانة للتبليغ عن الامر و محاولة التعامل معه""", user_id = 1)
                db.session.add(n)
                db.session.commit()
                flash("انت لم تسجل بعد", "warning")
                return redirect(url_for("user.login"))
    return checkit