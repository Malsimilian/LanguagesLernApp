@login_required
@app.route('/add_lesson/<int:course_id>', methods=['GET', 'POST'])
def add_lesson(course_id):
    form = LessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = Lesson(
            name=form.name.data,
            text_material=form.text.data,
            video_material=form.video.data,
            course_id=course_id
        )
        db_sess.add(lesson)
        db_sess.commit()
        return redirect(f'/my_course/{course_id}')
    return render_template('add_lesson.html', title='add_lesson', form=form)