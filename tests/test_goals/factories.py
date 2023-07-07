import factory.django


class CreateGoalCategoryRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalCommentRequest(factory.DictFactory):
    text = factory.Faker('sentence')
