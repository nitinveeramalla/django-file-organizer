from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import DirectoryPathForm, AnalyticsFilterForm
from .models import FileMetadata, ProcessingSession
from .file_organizer import FileOrganizer


def index(request):
    """Main page with directory input form"""
    if request.method == 'POST':
        form = DirectoryPathForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                input_directory = form.cleaned_data['directory_path']
                output_directory = form.cleaned_data.get('output_directory')
                
                # Create file organizer and process files
                organizer = FileOrganizer(input_directory, output_directory)
                results = organizer.organize_all_files()
                
                if results['success']:
                    messages.success(
                        request, 
                        f"Successfully organized {results['total_files']} files! "
                        f"Check the output directory: {results['output_directory']}"
                    )
                else:
                    messages.error(
                        request, 
                        f"Processing completed with {len(results['errors'])} errors. "
                        f"Check the details below."
                    )
                
                # Store results in session for display
                request.session['last_processing_results'] = results
                
                return redirect('organizer:results')
                
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = DirectoryPathForm()
    
    return render(request, 'organizer/index.html', {'form': form})


def results(request):
    """Display processing results"""
    results = request.session.get('last_processing_results', {})
    
    if not results:
        messages.info(request, "No processing results found. Please organize some files first.")
        return redirect('organizer:index')
    
    # Clear results from session after displaying
    if 'last_processing_results' in request.session:
        del request.session['last_processing_results']
    
    return render(request, 'organizer/results.html', {'results': results})


def analytics(request):
    """Display analytics dashboard"""
    # Get filter form
    filter_form = AnalyticsFilterForm(request.GET)
    
    # Base queryset
    files = FileMetadata.objects.all()
    
    # Apply filters
    if filter_form.is_valid():
        file_type = filter_form.cleaned_data.get('file_type')
        owner_name = filter_form.cleaned_data.get('owner_name')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        if file_type:
            files = files.filter(file_type=f'.{file_type}')
        
        if owner_name:
            files = files.filter(owner_name__icontains=owner_name)
        
        if date_from:
            files = files.filter(moved_at__date__gte=date_from)
        
        if date_to:
            files = files.filter(moved_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(files, 50)  # Show 50 files per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    stats = {
        'total_files': files.count(),
        'total_size': files.aggregate(total=Sum('file_size'))['total'] or 0,
        'files_by_type': dict(files.values('file_type').annotate(count=Count('id')).values_list('file_type', 'count')),
        'files_by_owner': dict(files.values('owner_name').annotate(count=Count('id')).values_list('owner_name', 'count')),
        'recent_sessions': ProcessingSession.objects.all()[:10],
    }
    
    context = {
        'filter_form': filter_form,
        'page_obj': page_obj,
        'stats': stats,
    }
    
    return render(request, 'organizer/analytics.html', context)


def analytics_api(request):
    """API endpoint for analytics data (for charts)"""
    if request.method == 'GET':
        # Get files by type for pie chart
        files_by_type = dict(
            FileMetadata.objects.values('file_type')
            .annotate(count=Count('id'))
            .values_list('file_type', 'count')
        )
        
        # Get files by owner for bar chart
        files_by_owner = dict(
            FileMetadata.objects.values('owner_name')
            .annotate(count=Count('id'))
            .values_list('owner_name', 'count')
        )
        
        # Get daily processing stats for line chart
        daily_stats = list(
            FileMetadata.objects.extra(
                select={'day': 'date(moved_at)'}
            ).values('day').annotate(count=Count('id')).order_by('day')
        )
        
        return JsonResponse({
            'files_by_type': files_by_type,
            'files_by_owner': files_by_owner,
            'daily_stats': daily_stats,
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def session_detail(request, session_id):
    """Display details of a specific processing session"""
    try:
        session = ProcessingSession.objects.get(session_id=session_id)
        files = FileMetadata.objects.filter(
            original_path__startswith=session.input_directory
        ).order_by('-moved_at')
        
        context = {
            'session': session,
            'files': files,
        }
        
        return render(request, 'organizer/session_detail.html', context)
        
    except ProcessingSession.DoesNotExist:
        messages.error(request, "Processing session not found.")
        return redirect('organizer:analytics')
