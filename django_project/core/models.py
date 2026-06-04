from django.db import models


class ContactSubmission(models.Model):
    SERVICE_CHOICES = [
        ('website', 'Website Development'),
        ('video', 'Video Editing'),
        ('graphic', 'Graphic Design'),
        ('branding', 'Logo & Branding'),
        ('other', 'Other'),
    ]
    BUDGET_CHOICES = [
        ('', '-- Select Budget Range --'),
        ('500', 'Under $500'),
        ('1000', '$500 - $1,000'),
        ('2500', '$1,000 - $2,500'),
        ('5000', '$2,500 - $5,000'),
        ('10000', '$5,000 - $10,000'),
        ('15000', '$10,000+'),
        ('flexible', 'Flexible / Not Sure'),
    ]
    TIMELINE_CHOICES = [
        ('', '-- Select Timeline --'),
        ('asap', 'ASAP (1-2 weeks)'),
        ('month', 'Within a Month'),
        ('months', '1-3 Months'),
        ('flexible', 'Flexible / Not Sure'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField('Phone Number (with country code)', max_length=20)
    country = models.CharField('Country', max_length=100, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='other')
    budget = models.CharField('Budget Range', max_length=20, choices=BUDGET_CHOICES, blank=True)
    timeline = models.CharField('Project Timeline', max_length=20, choices=TIMELINE_CHOICES, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f'{self.name} - {self.email}'


class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('website', 'Website Development'),
        ('video', 'Video Editing'),
        ('graphic', 'Graphic Design'),
        ('branding', 'Logo & Branding'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='portfolio/')
    project_url = models.URLField('Project URL', blank=True)
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = 'Portfolio Projects'

    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    platform = models.CharField(max_length=100)
    url = models.URLField()
    icon_class = models.CharField(
        'Font Awesome Icon Class',
        max_length=100,
        help_text='e.g. fa-brands fa-whatsapp, fa-solid fa-envelope',
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Social Media Links'

    def __str__(self):
        return self.platform


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.key
