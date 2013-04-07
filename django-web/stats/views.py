from django.http import HttpResponse
from django.shortcuts import render_to_response
import web.stats.stats as st

def stats(request,path):
  view_stats = "stats/view_stats.html"
  stats = st.Stats()
  stats.update()
  ctx = {"tree": stats.tree, "stats": stats}
  return render_to_response(view_stats,ctx)

